from django.urls import path
from .views import (
    HomeView, AboutView, ConceptDetailView,
    AddConceptCustomView, ConceptCreateView,
    ConceptUpdateView, ConceptDeleteView, UploadFileView, FieldOfStudyDetailView
)

app_name = 'cs'
urlpatterns = [
    path('',              HomeView.as_view(),       name='home'),
    path('about/',        AboutView.as_view(),      name='about'),
    path('concepts/<slug:concept_slug>/', ConceptDetailView.as_view(), name='concept_detail'),
    path('add-custom/',   AddConceptCustomView.as_view(), name='add_concept_custom'),
    path('add-model/',    ConceptCreateView.as_view(),   name='add_concept_model'),
    path('edit/<slug:concept_slug>/',   ConceptUpdateView.as_view(), name='edit_concept'),
    path('delete/<slug:concept_slug>/', ConceptDeleteView.as_view(), name='delete_concept'),
    path('upload/',       UploadFileView.as_view(),  name='upload_file'),
    path('field/<slug:field_of_study_slug>/', FieldOfStudyDetailView.as_view(), name='field_of_study_detail'),
]