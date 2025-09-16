from django.urls import path
from . import views
from . import converters
from django.urls import register_converter
from django.contrib import admin
from .views import add_concept_custom, add_concept_model, upload_file
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Панель Администрирования"
admin.site.index_title = "Управление сайтом"
admin.site.site_title = "Администрирование MyCSProject"

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('compare/', views.compare, name='compare'),
    path('concepts/', views.concepts_list, name='concepts'),
    path('concepts/<int:concept_id>/', views.concept_detail, name='concept_detail'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('go-home/', views.redirect_example, name='go_home'),
    path('hello/', views.get_params_example, name='hello'),
    path('category/<int:cat_id>/', views.category, name='category'),
    path('concept/<slug:concept_slug>/', views.concept_detail, name='concept_detail'),
    path('tags/', views.tags_list, name='tags_list'),
    path('admin/', admin.site.urls),
    path('add-custom/', add_concept_custom, name='add_concept_custom'),
    path('add-model/',  add_concept_model,  name='add_concept_model'),
    path('upload/', upload_file, name='upload_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'cs.views.custom_404'