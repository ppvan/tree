from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from tree.utils import hashed_filename
from user.models import User

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    label = models.CharField(max_length=255, unique=True, blank=False)
    image = ProcessedImageField(
        upload_to=hashed_filename,
        default="defaults/category.png",
        processors=[ResizeToFill(320, 320)],
        format="PNG",
        options={"quality": 60},
    )
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label


class Product(BaseModel):
    name = models.CharField(max_length=255, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(0)]
    )
    summary = models.TextField(default="")
    description = models.TextField(default="")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = ProcessedImageField(
        upload_to=hashed_filename,
        default="defaults/product.png",
        processors=[ResizeToFill(400, 400)],
        format="PNG",
        options={"quality": 60},
    )

    class Meta:
        unique_together = ("name", "category")

    def state(self):
        return "Còn hàng" if self.quantity > 0 else "Hết hàng"

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "code")

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "code", "province")

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "code", "district")

    def __str__(self):
        return self.name


class Address(BaseModel):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address2} - {self.address1}"


class Order(BaseModel):
    PENDING = "PE"
    DELIVERY = "DE"
    COMPLETED = "CO"
    CANCEL = "CA"
    VERIFY = "VE"

    ORDER_STATUS = [
        (PENDING, "Giỏ hàng"),
        (VERIFY, "Chờ xác nhận"),
        (DELIVERY, "Đang giao"),
        (COMPLETED, "Hoàn thành"),
        (CANCEL, "Đã hủy"),
    ]

    state = models.CharField(max_length=2, choices=ORDER_STATUS, default=PENDING)
    user = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (self.user.username, self.state).__str__()

    def price(self):
        return sum(item.total_price() for item in self.items.all())

    def total_price(self):
        return self.price() + self.delivery_fee

    def not_completed(self):
        return self.state == self.DELIVERY

    def size(self):
        return self.items.count()

    def cancellable(self):
        return self.state == self.PENDING or self.state == self.VERIFY


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity


class Payment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.order} - {self.amount}"
