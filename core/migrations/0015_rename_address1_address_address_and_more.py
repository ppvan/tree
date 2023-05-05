# Generated by Django 4.2.1 on 2023-05-05 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_address_ward_order_items"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="address1",
            new_name="address",
        ),
        migrations.RemoveField(
            model_name="address",
            name="address2",
        ),
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.OneToOneField(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="core.address",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
