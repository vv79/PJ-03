from django import forms
from .models import Announcement, Category, Response


class AnnouncementForm(forms.ModelForm):
    category = forms.Select(
        choices=Category.objects.all()
    )

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category']
        labels = {
            "title": "Title",
            "content": "Content",
            "categories": "Categories",
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        labels = {
            "content": "Content",
        }
