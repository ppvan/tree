import uuid
from pathlib import Path

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from user.models import User

# Create your models here.

MEDIA_PATH = Path("product_images")


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Product(BaseModel):
    def get_path(instance, filename):
        extension = filename.split(".")[-1]
        uuid_name = uuid.uuid1().hex
        return MEDIA_PATH / f"{uuid_name}.{extension}"

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    summary = models.TextField(default="")
    description = models.TextField(default="")
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=True, null=False
    )
    thumbnail = ProcessedImageField(
        upload_to=get_path,
        default="product_images/default.png",
        processors=[ResizeToFill(400, 400)],
        format="PNG",
        options={"quality": 60},
    )

    def state(self):
        return "Còn hàng" if self.quantity > 0 else "Hết hàng"

    def __str__(self):
        return self.name


class Address(BaseModel):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    # user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address1} - {self.address2}"


class Order(BaseModel):
    PENDING = "PE"
    DELIVERY = "DE"
    COMPLETED = "CO"
    CANCEL = "CA"

    ORDER_STATUS = [
        (PENDING, "Chưa xác nhận"),
        (DELIVERY, "Đang giao"),
        (COMPLETED, "Hoàn thành"),
        (CANCEL, "Đã hủy"),
    ]

    state = models.CharField(max_length=2, choices=ORDER_STATUS, default=PENDING)
    user = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    # address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (self.user.username, self.state).__str__()

    def total_price(self):
        return sum(item.total_price() for item in self.orderitem_set.all())


class Payment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.order} - {self.amount}"


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price
