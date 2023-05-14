from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from tree.utils import hashed_filename


class Post(models.Model):
    BUG_REPORT = "bug"
    BLOG = "blog"

    POST_TYPE = (
        (BLOG, "Blog"),
        (BUG_REPORT, "Bug Report"),
    )

    title = models.CharField(max_length=200)
    cover_image = ProcessedImageField(
        upload_to=hashed_filename,
        default="defaults/post.jpg",
        processors=[ResizeToFill(320, 240)],
        format="JPEG",
        options={"quality": 60},
    )
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default="blog")

    def __str__(self) -> str:
        return self.title

    def markdown(self):
        return markdownify(self.content)
