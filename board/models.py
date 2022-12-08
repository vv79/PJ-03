from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

    class Meta:
        db_table = "board_category"
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "board_category_subscriber"
        verbose_name = 'Category subscriber'
        verbose_name_plural = 'Category subscribers'


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, )
    content = RichTextField()

    class Meta:
        db_table = "board_announcement"
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])


class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "board_announcement_response"
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'

    def get_absolute_url(self):
        return reverse('response_detail', args=[str(self.id)])
