# Generated by Django 4.2.1 on 2023-05-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_auto_20230509_1453"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_fee",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="state",
            field=models.CharField(
                choices=[
                    ("PE", "Chưa xác nhận"),
                    ("VE", "Đã xác nhận"),
                    ("DE", "Đang giao"),
                    ("CO", "Hoàn thành"),
                    ("CA", "Đã hủy"),
                ],
                default="PE",
                max_length=2,
            ),
        ),
    ]
