from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse

def index(request):
    return render(request, 'cs/index.html')

def about(request):
    return render(request, 'cs/about.html')

def compare(request):
    return render(request, 'cs/compare.html')

def cs_list(request):
    all_cs_topics = [
        {'id': 1, 'name': 'Искусственный интеллект', 'description': 'Область компьютерных наук, изучающая методы создания интеллектуальных агентов.'},
        {'id': 2, 'name': 'Машинное обучение', 'description': 'Подраздел искусственного интеллекта, изучающий методы построения алгоритмов, способных обучаться на данных.'},
        {'id': 3, 'name': 'Веб-разработка', 'description': 'Процесс создания веб-сайтов и веб-приложений.'},
        {'id': 4, 'name': 'Базы данных', 'description': 'Организованная коллекция данных, предназначенная для эффективного хранения и извлечения.'},
    ]
    return render(request, 'cs/cs_list.html', {'cs_topics': all_cs_topics})

def cs_detail(request, topic_id):
    if topic_id > 10:
        raise Http404("Тема с таким ID не найдена")
    return HttpResponse(f"<h1>Информация о теме</h1><p>ID: {topic_id}</p>")

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