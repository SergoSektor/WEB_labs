from django.views.generic.base import ContextMixin

MENU = [
    {'title': 'Главная',              'url_name': 'cs:home'},
    {'title': 'О сайте',              'url_name': 'cs:about'},
    {'title': 'Добавить (Form)',      'url_name': 'cs:add_concept_custom'},
    {'title': 'Добавить (ModelForm)', 'url_name': 'cs:add_concept_model'},
    {'title': 'Загрузка файла',       'url_name': 'cs:upload_file'},
]

class DataMixin(ContextMixin):
    """
    Добавляет в контекст:
      - global menu
      - title, если задано
      - page_range для ListView с пагинацией
    """
    title = None

    def get_context_data(self, *, object_list=None, **kwargs):
        # Сначала получаем весь контекст от родительских классов,
        # в том числе paginator, page_obj, object_list
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Базовый контекст
        context['menu'] = MENU
        if self.title:
            context['title'] = self.title

        # Если есть пагинация — вычисляем ограниченный диапазон страниц
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        if paginator and page_obj:
            total = paginator.num_pages
            current = page_obj.number
            window = 2
            start = max(current - window, 1)
            end   = min(current + window, total)
            context['page_range'] = range(start, end + 1)

        return context

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def resize_image(image_field, size=(512, 512), quality=80):
    if not image_field:
        return image_field

    img = Image.open(image_field)
    img.thumbnail(size, Image.LANCZOS)

    # Создаем буфер для сохранения изображения
    thumb_io = BytesIO()
    img_format = img.format if img.format else 'JPEG' # Определяем формат или по умолчанию JPEG
    img.save(thumb_io, format=img_format, quality=quality)
    thumb_io.seek(0)

    # Создаем новый InMemoryUploadedFile, чтобы его можно было сохранить
    new_image = InMemoryUploadedFile(
        thumb_io,
        'ImageField',
        image_field.name, # Сохраняем оригинальное имя файла
        f'image/{img_format.lower()}', # Определяем content_type на основе формата Pillow
        thumb_io.tell(),
        None
    )
    return new_image