from django import template
from anime.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    """Тэг для подключения всех категорий"""
    return Category.objects.all()
