from django.db import models
from django.urls import reverse

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

    objects = models.Manager()         # Стандартный менеджер
    published = PublishedManager()       # Пользовательский менеджер для опубликованных записей

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = "Концепция компьютерных наук"
        verbose_name_plural = "Концепции компьютерных наук"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concept_detail', kwargs={'concept_slug': self.slug})
