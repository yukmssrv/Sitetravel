from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Country, Category, TagPost, ExtraInfo, Attraction
from .utils import DataMixin


class ExtraInfoFilter(admin.SimpleListFilter):
    title = 'Доп. информация'
    parameter_name = 'extrainfo_status'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Есть доп. информация'),
            ('no', 'Нет доп. информации'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(extrainfo__isnull=False)
        if self.value() == 'no':
            return queryset.filter(extrainfo__isnull=True)
        return queryset

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat', 'has_extra_info')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 10
    actions = ['make_published', 'make_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat', 'is_published', 'time_create', ExtraInfoFilter]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'photo')
        }),
        ('Категория и теги', {
            'fields': ('cat', 'tags')
        }),
        ('Дополнительная информация', {
            'fields': ('extrainfo',)
        }),
    )
    #readonly_fields = ['slug', 'post_photo']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['slug', 'post_photo']
        return []
    filter_horizontal = ['tags']


    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, obj):
        return f"Длина текста: {len(obj.content)} символов"

    @admin.display(description="Доп. информация", boolean=True)
    def has_extra_info(self, obj):
        return hasattr(obj, 'extrainfo') and obj.extrainfo is not None

    @admin.action(description="Опубликовать выбранные страны")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} страна(ы) опубликована(ы).", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные страны")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} страна(ы) снята(ы) с публикации.", messages.WARNING)

    @admin.display(description="Изображение")
    def post_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover;">')
        return "Без фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ('name',)

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    ordering = ('tag',)

@admin.register(ExtraInfo)
class ExtraInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'capital', 'population')
    list_display_links = ('id', 'capital')


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'slug')
    list_display_links = ('title',)
    search_fields = ('title', 'country__title')
    list_filter = ('country',)



