from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
import os
import uuid
from .models import ComputerScienceConcept, FieldOfStudy, Tag

# 1. Собственный валидатор: запрет цифр в названии
def validate_title_no_digits(value):
    if any(ch.isdigit() for ch in value):
        raise forms.ValidationError(
            'Название не должно содержать цифр',
            code='no_digits'
        )

# 2. Собственный валидатор: запрет слова "test"
def validate_no_test(value):
    if 'test' in value.lower():
        raise forms.ValidationError(
            'Слово "test" запрещено в названии',
            code='no_test'
        )

# Несвязанная с моделью форма
class ConceptForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label='Название концепции компьютерных наук',
        validators=[validate_title_no_digits],
        help_text='До 255 символов, без цифр'
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Описание',
        help_text='Дополнительная информация (необязательно)'
    )
    difficulty = forms.IntegerField(
        label='Сложность (от 1 до 5)',
        min_value=1,
        max_value=5,
        help_text='Число от 1 до 5'
    )
    image = forms.ImageField(
        required=False,
        label='Изображение',
        help_text='JPG/PNG до 5 МБ'
    )

# Форма, связанная с моделью
class ConceptModelForm(forms.ModelForm):
    # Переопределяем title, чтобы применить оба валидатора
    title = forms.CharField(
        max_length=255,
        label='Название концепции компьютерных наук',
        validators=[validate_no_test, validate_title_no_digits],
        help_text='Без цифр и слова "test"'
    )

    difficulty = forms.IntegerField(
        label='Сложность (от 1 до 5)',
        min_value=1,
        max_value=5,
        help_text='Число от 1 до 5'
    )

    class Meta:
        model = ComputerScienceConcept
        fields = [
            'title',
            'slug',
            'description',
            'difficulty',
            'field_of_study',
            'tags',
            'image',
        ]
        widgets = {
            'description': forms.Textarea,
        }


class UploadForm(forms.Form):
    file = forms.FileField(
        label='Выберите файл',
        help_text='Максимум 10 МБ. Любой тип.'
    )

    def clean_file(self):
        f = self.cleaned_data['file']
        if f.size > 10 * 1024 * 1024:
            raise forms.ValidationError('Файл слишком большой (больше 10 МБ)')
        return f

    def save_file(self):
        f = self.cleaned_data['file']
        ext = os.path.splitext(f.name)[1]
        new_name = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join('uploads', new_name)
        saved_path = default_storage.save(path, f)
        return settings.MEDIA_URL + saved_path
