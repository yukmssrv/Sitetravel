from django import template
from django.db.models import Count
from country.models import TagPost

register = template.Library()

# Список категорий
cats_db = [
    {'id': 1, 'name': 'Архитектура'},
    {'id': 2, 'name': 'Природа'},
    {'id': 3, 'name': 'Музеи'},
]

@register.inclusion_tag('country/list_categories.html')
def show_categories(cat_selected=0):
    return {'categories': cats_db, 'cat_selected': cat_selected}


@register.inclusion_tag('country/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count('countries')).filter(total__gt=0)
    return {'tags': tags}