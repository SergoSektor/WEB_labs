from django import template

# Пример фиктивного списка категорий
categories_db = [
    {'id': 1, 'name': 'Программирование'},
    {'id': 2, 'name': 'Алгоритмы'},
    {'id': 3, 'name': 'Базы данных'},
    {'id': 4, 'name': 'Искусственный интеллект'},
]

register = template.Library()

@register.simple_tag()
def get_categories():
    return categories_db
