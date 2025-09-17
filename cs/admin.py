from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.html import mark_safe
from django.db.models import ExpressionWrapper, F, DecimalField

from .models import ComputerScienceConcept, FieldOfStudy, ConceptDetail, Tag

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Управление сайтом"
admin.site.site_title = "Администрирование Computer Science Project"

# Пользовательское вычисляемое поле: краткая информация
@admin.display(description="Краткая информация")
def brief_info(obj):
    return f"Описание: {len(obj.description)} символов" if obj.description else "Нет описания"


# Пользовательское вычисляемое поле: сложность
@admin.display(description="Сложность")
def display_difficulty(obj):
    if obj.difficulty is not None:
        return f"{obj.difficulty}/5"
    return "N/A"


# Кастомный фильтр для статуса публикации
class PublishedFilter(SimpleListFilter):
    title = "Статус публикации"
    parameter_name = "pub_status"

    def lookups(self, request, model_admin):
        return [
            ("published", "Опубликовано"),
            ("draft", "Черновик"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "published":
            return queryset.filter(is_published=ComputerScienceConcept.Status.PUBLISHED)
        elif self.value() == "draft":
            return queryset.filter(is_published=ComputerScienceConcept.Status.DRAFT)
        return queryset


# Дополнительный кастомный фильтр по диапазону сложности
class DifficultyRangeFilter(SimpleListFilter):
    title = "Диапазон сложности"
    parameter_name = "difficulty_range"

    def lookups(self, request, model_admin):
        return [
            ('low', 'Низкая (1-2)'),
            ('medium', 'Средняя (3)'),
            ('high', 'Высокая (4-5)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(difficulty__lte=2)
        elif self.value() == 'medium':
            return queryset.filter(difficulty=3)
        elif self.value() == 'high':
            return queryset.filter(difficulty__gte=4)
        return queryset


@admin.register(ComputerScienceConcept)
class ComputerScienceConceptAdmin(admin.ModelAdmin):
    # Поля для формы добавления/редактирования
    fields = [
        'title', 'slug', 'description', 'difficulty',
        'field_of_study', 'tags', 'image', 'image_preview'
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['time_create', 'time_update', 'image_preview']

    # Список записей
    list_display = (
        'id', 'title', 'field_of_study', 'time_create',
        'is_published', brief_info, display_difficulty,
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 5
    search_fields = ['title', 'field_of_study__name']
    list_filter = [PublishedFilter, 'field_of_study', DifficultyRangeFilter]
    actions = ['set_published', 'set_draft']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=ComputerScienceConcept.Status.PUBLISHED)
        self.message_user(request, f"Статус 'Опубликовано' обновлён для {count} записей.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=ComputerScienceConcept.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации.", messages.WARNING)

    @admin.display(description='Превью изображения')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' style='max-height:200px;' />")
        return "(нет изображения)"


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

    search_fields = ('name', 'description')


@admin.register(ConceptDetail)
class ConceptDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'concept', 'core_technologies', 'prerequisites', 'estimated_learning_time')
    list_display_links = ('id', 'concept')
    search_fields = ('concept__title', 'core_technologies', 'prerequisites')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
