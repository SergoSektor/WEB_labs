from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
import uuid

from .models import ComputerScienceConcept, Tag, FieldOfStudy # Updated model import
from .forms import ConceptForm, ConceptModelForm, UploadForm # Updated import

def index(request):
    concepts = ComputerScienceConcept.published.all()
    return render(request, 'cs/index.html', {
        'title': 'Главная страница',
        'concepts': concepts,
    })

def about(request):
    return render(request, 'cs/about.html')

def compare(request):
    return render(request, 'cs/compare.html')

def concepts_list(request):
    all_concepts = [
        {'id': 1, 'name': 'Data Structures', 'description': 'Fundamental ways to organize data.'},
        {'id': 2, 'name': 'Algorithms', 'description': 'Step-by-step procedures for calculations.'},
    ]
    return render(request, 'cs/cs_list.html', {'concepts': all_concepts})

def concept_detail(request, concept_slug):
    concept = get_object_or_404(ComputerScienceConcept, slug=concept_slug)
    return render(request, 'cs/concept_detail.html', {
        'title': concept.title,
        'concept': concept,
    })

def archive(request, year):
    if year > 2025:
        raise Http404("Нет данных за этот год")
    return HttpResponse(f"<h1>Архив за {year} год</h1>")

def redirect_example(request):
    return redirect('home')

def get_params_example(request):
    name = request.GET.get('name', 'Гость')
    return HttpResponse(f"<h1>Привет, {name}!</h1>")

def category(request, cat_id):
    return HttpResponse(f"<h1>Страница категории</h1><p>ID категории: {cat_id}</p>")

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'cs/tags_list.html', {
        'title': 'Теги',
        'tags': tags,
    })

def add_concept_custom(request):
    """
    Пункт 1: форма ConceptForm (несвязанная с моделью) с поддержкой загрузки изображения.
    """
    if request.method == 'POST':
        form = ConceptForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            concept = ComputerScienceConcept.objects.create(
                title=cd['title'],
                # slug=cd['title'].lower().replace(' ', '-'), # Слаг теперь генерируется в модели
                description=cd['description'],
                difficulty=cd['difficulty'],
                is_published=ComputerScienceConcept.Status.DRAFT
            )
            # Сохраняем изображение, если пользователь его загрузил
            image = cd.get('image')
            if image:
                concept.image = image
                concept.save()
            return redirect(concept.get_absolute_url())
    else:
        form = ConceptForm()

    return render(request, 'cs/add_concept_custom.html', {'form': form})


def add_concept_model(request):
    """
    Пункт 2: форма ConceptModelForm (ModelForm) с поддержкой загрузки изображения.
    """
    if request.method == 'POST':
        form = ConceptModelForm(request.POST, request.FILES)
        if form.is_valid():
            concept = form.save(commit=False)
            concept.is_published = ComputerScienceConcept.Status.DRAFT
            concept.save()
            form.save_m2m()  # сохраняем M2M-поля (tags) и image
            return redirect(concept.get_absolute_url())
    else:
        form = ConceptModelForm()

    return render(request, 'cs/add_concept_model.html', {'form': form})


def upload_file(request):
    """
    Обрабатывает UploadForm, сохраняет файл с случайным именем
    и выводит пользователю ссылку на загруженный файл.
    """
    link = None

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            ext = os.path.splitext(f.name)[1]
            new_name = f"{uuid.uuid4().hex}{ext}"

            path = os.path.join('uploads', new_name)
            saved_path = default_storage.save(path, f)

            link = settings.MEDIA_URL + saved_path

    else:
        form = UploadForm()

    return render(request, 'cs/upload.html', {
        'form': form,
        'link': link,
    })