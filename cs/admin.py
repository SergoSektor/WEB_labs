from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from .models import ComputerScienceConcept, FieldOfStudy, ConceptDetail, Tag

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Управление сайтом"
admin.site.site_title = "Администрирование Computer Science Project"

# Функция для вычисляемого поля "Краткая информация"
@admin.display(description="Краткая информация")
def brief_info(obj):
    return f"Описание: {len(obj.description)} символов" if obj.description else "Нет описания"

# Пользовательское вычисляемое поле: уровень сложности
@admin.display(description="Уровень сложности")
def difficulty_level(obj):
    if obj.difficulty is not None:
        return f"Сложность: {obj.difficulty}/5"
    return "Не указана"

# Пользовательское вычисляемое поле: оценочное время изучения (часы)
@admin.display(description="Оценочное время изучения (часы)")
def estimated_reading_time(obj):
    if hasattr(obj, 'detail') and obj.detail.estimated_learning_time is not None:
        return f"{obj.detail.estimated_learning_time} часов"
    return "Не указано"

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
    title = "Диапазон сложности"  # Заголовок фильтра в админ-панели
    parameter_name = "difficulty_range"  # Параметр в URL

    def lookups(self, request, model_admin):
        return [
            ('easy', 'Легкая (1-2)'),
            ('medium', 'Средняя (3)'),
            ('hard', 'Сложная (4-5)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'easy':
            return queryset.filter(difficulty__lte=2)
        elif self.value() == 'medium':
            return queryset.filter(difficulty=3)
        elif self.value() == 'hard':
            return queryset.filter(difficulty__gte=4)
        return queryset

@admin.register(ComputerScienceConcept)
class ComputerScienceConceptAdmin(admin.ModelAdmin):
    # Настройка формы добавления/редактирования записей:
    # Поля, отображаемые в форме, перечисляются в указанном порядке.
    fields = ('title', 'slug', 'description', 'difficulty', 'field_of_study', 'tags', 'is_published')
    # Автоматическая генерация поля slug на основе поля title.
    prepopulated_fields = {"slug": ("title",)}
    # Поля, которые доступны только для чтения
    readonly_fields = ['time_create', 'time_update']


    list_display = (
        'id',
        'title',
        'field_of_study',
        'time_create',
        'is_published',
        brief_info,
        difficulty_level,
        estimated_reading_time,
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    search_fields = ('title', 'field_of_study__name')
    list_filter = [PublishedFilter, 'field_of_study', DifficultyRangeFilter]
    list_per_page = 5

    # Пользовательское действие для установки статуса "Опубликовано"
    @admin.action(description="Опубликовать выбранные концепции")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=ComputerScienceConcept.Status.PUBLISHED)
        self.message_user(request, f"Статус 'Опубликовано' обновлён для {count} концепций.", messages.SUCCESS)

    # Пользовательское действие для установки статуса "Черновик"
    @admin.action(description="Снять с публикации выбранные концепции")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=ComputerScienceConcept.Status.DRAFT)
        self.message_user(request, f"{count} концепций сняты с публикации.", messages.WARNING)

    actions = ['set_published', 'set_draft']

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

@admin.register(ConceptDetail)
class ConceptDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'concept', 'core_technologies', 'estimated_learning_time')
    list_display_links = ('id', 'concept')
    search_fields = ('concept__title', 'core_technologies')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
