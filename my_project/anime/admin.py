from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Ip)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    """Сортированное отображение аниме"""
    list_display = ('id', 'title', 'count_views', 'created_at', 'get_image', 'display_categories')
    list_display_links = ('id', 'title')
    list_filter = ('id', 'category')

    def get_image(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width=75>')
            except:
                return '-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение комментариев"""
    list_display = ('id', 'user', 'anime', 'created_at')
    list_display_links = ('id', 'user')

