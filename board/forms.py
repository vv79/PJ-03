from django import forms
from .models import Post, Category
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    categories = forms.SelectMultiple(
        choices=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        labels = {
            "title": _("Title"),
            "content": _("Content"),
            "categories": _("Categories"),
        }
