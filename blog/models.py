import uuid
from pathlib import Path

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from tree.utils import hashed_filename
from markdownx.models import MarkdownxField


class Post(models.Model):
    title = models.CharField(max_length=200)
    cover_image = ProcessedImageField(
        upload_to=hashed_filename,
        default="posts/default.jpg",
        processors=[ResizeToFill(320, 240)],
        format="JPEG",
        options={"quality": 60},
    )
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
