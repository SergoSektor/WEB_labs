from django import template
from cs.models import FieldOfStudy # Импортируем модель FieldOfStudy

register = template.Library()

@register.simple_tag()
def get_categories():
    return FieldOfStudy.objects.all() # Возвращаем все объекты FieldOfStudy
