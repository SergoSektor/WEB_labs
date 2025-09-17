from django.db import models
from django.urls import reverse
from django.utils.text import slugify # Импортируем slugify
from .utils import resize_image # Импортируем функцию изменения размера изображения

# Модель для областей компьютерных наук
class FieldOfStudy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Область науки")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание области")

    class Meta:
        verbose_name = "Область науки"
        verbose_name_plural = "Области науки"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Проверяем уникальность слага
            base_slug = self.slug
            num = 1
            while FieldOfStudy.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{num}"
                num += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cs:field_of_study_detail', kwargs={'field_of_study_slug': self.slug})

# Пользовательский менеджер для выборки только опубликованных записей
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Фильтруем записи по полю публикации с использованием перечисления
        return super().get_queryset().filter(is_published=ComputerScienceConcept.Status.PUBLISHED)

class ComputerScienceConcept(models.Model):
    # Класс-перечисление для статуса публикации
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название концепции")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    difficulty = models.IntegerField(default=1, verbose_name="Сложность (от 1 до 5)") # Новое поле для сложности
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Публикация")
    image = models.ImageField(upload_to='concept_images/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение') # New field

    # Связь один-ко-многим с FieldOfStudy
    field_of_study = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.CASCADE,
        related_name='concepts',
        verbose_name="Область науки",
        null=True,
        blank=True
    )

    objects = models.Manager()         # Стандартный менеджер
    published = PublishedManager()       # Пользовательский менеджер для опубликованных записей

    class Meta:
        permissions = [
            ('can_publish_concept', 'Может публиковать концепцию'),
        ]
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = "Концепция компьютерных наук"
        verbose_name_plural = "Концепции компьютерных наук"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Проверяем уникальность слага
            base_slug = self.slug
            num = 1
            while ComputerScienceConcept.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{num}"
                num += 1

        # Обработка изменения размера изображения, если изображение присутствует
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cs:concept_detail', kwargs={'concept_slug': self.slug})

# Модель для расширенной информации о концепции (OneToOne)
class ConceptDetail(models.Model):
    concept = models.OneToOneField(
        ComputerScienceConcept,
        on_delete=models.CASCADE,
        related_name='detail',
        verbose_name="Концепция"
    )
    core_technologies = models.TextField(blank=True, verbose_name="Ключевые технологии")
    prerequisites = models.TextField(blank=True, verbose_name="Предварительные условия")
    estimated_learning_time = models.PositiveIntegerField(verbose_name="Примерное время изучения (часы)", null=True, blank=True)

    class Meta:
        verbose_name = "Детали концепции"
        verbose_name_plural = "Детали концепций"

    def __str__(self):
        return f"Детали {self.concept.title}"

# Модель для тегов (Many-to-Many)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL тега") # Убрал default='default-slug'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cs:concepts_by_tag', kwargs={'tag_slug': self.slug})

# Добавляем ManyToManyField в ComputerScienceConcept после определения Tag
ComputerScienceConcept.add_to_class('tags', models.ManyToManyField(
    Tag,
    related_name='concepts',
    verbose_name="Теги",
    blank=True
))

# Модель для комментариев
from django.contrib.auth import get_user_model
User = get_user_model()

class Comment(models.Model):
    concept   = models.ForeignKey(ComputerScienceConcept, on_delete=models.CASCADE, related_name='comments', verbose_name='Концепция')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text    = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий от {self.author} к {self.concept.title}"