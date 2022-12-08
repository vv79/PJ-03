from django.contrib import admin
from .models import Category, Announcement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement
    list_display = ('title', 'author', 'date_created')
    list_filter = ('title', 'author', 'date_created')
    search_fields = ('title', 'author__user__first_name', 'author__user__last_name', 'author__user__username')
    date_hierarchy = 'date_created'
