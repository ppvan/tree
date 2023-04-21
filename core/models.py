import uuid
from pathlib import Path

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

MEDIA_PATH = Path("product_images")


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    summary = models.TextField()

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    def get_path(instance, filename):
        extension = filename.split(".")[-1]
        uuid_name = uuid.uuid1().hex
        return MEDIA_PATH / f"{uuid_name}.{extension}"

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to=get_path,
        default="avatars/default.png",
        processors=[ResizeToFill(400, 400)],
        format="PNG",
        options={"quality": 60},
    )

    def __str__(self):
        return f"{self.product.name} - {self.image.url}"


class Category(BaseModel):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Address(BaseModel):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    # user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address1} - {self.address2}"


class Order(BaseModel):
    # user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
