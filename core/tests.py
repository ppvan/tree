from django.db import IntegrityError
from django.test import TestCase
from .models import Product, Category
from django.core.exceptions import ValidationError

# Create your tests here.


class AddProductTest(TestCase):
    def setUp(self):
        pass

    def test_add_product(self):
        """Positive test case for adding a product"""
        product = Product.objects.create(
            name="Test Product",
            price=100000,
            summary="Test Summary",
            description="Test Description",
            quantity=10,
            category=Category.objects.create(label="Test Category"),
        )
        product.save()

    def test_add_product_with_invalid_price(self):
        """Negative test case for adding a product with invalid price"""
        product = Product.objects.create(
            name="Test Product",
            price=-100000,
            summary="Test Summary",
            description="Test Description",
            quantity=10,
            category=Category.objects.create(label="Test Category"),
        )
        self.assertRaises(ValidationError, product.full_clean)

    def test_add_product_with_invalid_quantity(self):
        """Negative test case for adding a product with invalid quantity"""
        with self.assertRaises(IntegrityError) as context:
            product = Product.objects.create(
                name="Test Product",
                price=100000,
                summary="Test Summary",
                description="Test Description",
                quantity=-10,
                category=Category.objects.create(label="Test Category"),
            )
            product.save()
            self.assertTrue("CHECK constraint failed" in str(context.exception))

    def test_add_product_with_invalid_category(self):
        """Negative test case for adding a product with invalid category"""
        with self.assertRaises(IntegrityError) as context:
            product = Product.objects.create(
                name="Test Product",
                price=100000,
                summary="Test Summary",
                description="Test Description",
                quantity=10,
            )
            product.save()
            self.assertTrue("NOT NULL constraint failed" in str(context.exception))


class CategoryTest(TestCase):
    def setUp(self):
        pass

    def test_add_category(self):
        """Positive test case for adding a category"""
        category = Category.objects.create(label="Test Category")
        category.save()

    def test_add_category_with_invalid_label(self):
        """Negative test case for adding a category with invalid label"""
        category = Category.objects.create(label="")
        self.assertRaises(ValidationError, category.full_clean)
