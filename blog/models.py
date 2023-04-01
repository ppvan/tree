from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.


class MyModel(models.Model):
    content = MarkdownxField()
