# Generated by Django 4.2.1 on 2023-05-05 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import tree.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email_confirmed", models.BooleanField(default=False)),
                (
                    "avatar",
                    imagekit.models.fields.ProcessedImageField(
                        default="defaults/avatar.png",
                        upload_to=tree.utils.hashed_filename,
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
