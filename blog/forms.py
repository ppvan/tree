from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "cover_image", "content"]

        widgets = {
            "content": forms.Textarea(attrs={"cols": 60}),
        }
