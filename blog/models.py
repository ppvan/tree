from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

import uuid
from pathlib import Path

# Create your models here.

MEDIA_PATH = Path('posts')


class Post(models.Model):

    # FIXME: This should not up here, must below fields declaration
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        uuid_name = uuid.uuid1().hex
        return MEDIA_PATH / f'{uuid_name}.{extension}'

    title = models.CharField(max_length=200)
    cover_image = ProcessedImageField(upload_to=get_path,
                                      default='posts/default.jpg',
                                      processors=[ResizeToFill(320, 240)],
                                      format='JPEG',
                                      options={'quality': 60})
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
