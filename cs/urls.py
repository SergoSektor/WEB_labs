from django.urls import path
from . import views
from . import converters
from django.urls import register_converter

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),           # Главная страница
    path('about/', views.about, name='about'),      # О нас
    path('compare/', views.compare, name='compare'), # Сравнение
    path('cs/', views.cs_list, name='cs'),      # Список тем
    path('cs/<int:topic_id>/', views.cs_detail, name='cs_detail'),  # Детальная страница темы
    path('concept/<slug:concept_slug>/', views.cs_detail, name='concept_detail'),  # Детальная страница концепции
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('go-home/', views.redirect_example, name='go_home'),
    path('hello/', views.get_params_example, name='hello'),
    path('category/<int:cat_id>/', views.category, name='category'),
]

handler404 = 'cs.views.custom_404'