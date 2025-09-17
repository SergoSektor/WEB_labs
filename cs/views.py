from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    FormView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ComputerScienceConcept, FieldOfStudy, Tag
from .forms import ConceptForm, ConceptModelForm, UploadForm, CommentForm
from .utils import DataMixin


class HomeView(DataMixin, ListView):
    model = ComputerScienceConcept
    template_name = 'cs/index.html'
    context_object_name = 'concepts'
    paginate_by = 5
    queryset = ComputerScienceConcept.published.all()
    title = 'Главная'


class AboutView(DataMixin, TemplateView):
    template_name = 'cs/about.html'
    title = 'О сайте'


class ConceptDetailView(DataMixin, DetailView):
    model = ComputerScienceConcept
    template_name = 'cs/concept_detail.html'
    context_object_name = 'concept'
    slug_field = 'slug'
    slug_url_kwarg = 'concept_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        concept = self.get_object()
        context['title'] = concept.title
        context['comments'] = concept.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.concept = self.object
            comment.author = request.user
            comment.save()
            return self.get(request, *args, **kwargs) # Возвращаемся к GET запросу после успешной отправки
        else:
            # Если форма недействительна, возвращаем ее с ошибками
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class AddConceptCustomView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ConceptForm
    template_name = 'cs/add_concept_custom.html'
    success_url = reverse_lazy('cs:home')
    title = 'Добавить (Form)'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        cd = form.cleaned_data
        concept = ComputerScienceConcept.objects.create(
            title=cd['title'],
            slug=cd['title'].lower().replace(' ', '-'),
            description=cd['description'],
            difficulty=cd['difficulty'],
            is_published=ComputerScienceConcept.Status.DRAFT
        )
        image = cd.get('image')
        if image:
            concept.image = image
            concept.save()
        return super().form_valid(form)


class ConceptCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = ComputerScienceConcept
    form_class = ConceptModelForm
    template_name = 'cs/add_concept_model.html'
    success_url = reverse_lazy('cs:home')
    title = 'Добавить (ModelForm)'
    login_url = reverse_lazy('users:login')


class ConceptUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = ComputerScienceConcept
    form_class = ConceptModelForm
    template_name = 'cs/add_concept_model.html'
    success_url = reverse_lazy('cs:home')
    slug_field = 'slug'
    slug_url_kwarg = 'concept_slug'
    title = 'Редактировать концепцию'
    login_url = reverse_lazy('users:login')


class ConceptDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = ComputerScienceConcept
    template_name = 'cs/concept_confirm_delete.html'
    success_url = reverse_lazy('cs:home')
    slug_field = 'slug'
    slug_url_kwarg = 'concept_slug'
    title = 'Удалить концепцию'
    login_url = reverse_lazy('users:login')


class UploadFileView(LoginRequiredMixin, DataMixin, FormView):
    form_class = UploadForm
    template_name = 'cs/upload.html'
    success_url = reverse_lazy('cs:upload_file')
    title = 'Загрузка файла'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save_file()
        return super().form_valid(form)


class FieldOfStudyDetailView(DataMixin, ListView):
    model = ComputerScienceConcept
    template_name = 'cs/field_of_study_detail.html' # Шаблон для отображения концепций по области
    context_object_name = 'concepts'
    paginate_by = 5

    def get_queryset(self):
        # Получаем слаг области науки из URL
        field_of_study_slug = self.kwargs['field_of_study_slug']
        # Фильтруем концепции по этой области
        return ComputerScienceConcept.published.filter(field_of_study__slug=field_of_study_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем объект FieldOfStudy, чтобы отобразить его название
        field_of_study_slug = self.kwargs['field_of_study_slug']
        field_of_study = FieldOfStudy.objects.get(slug=field_of_study_slug)
        context['title'] = f"Концепции в области: {field_of_study.name}"
        context['field_of_study'] = field_of_study
        return context


class CompareConceptsView(DataMixin, TemplateView):
    template_name = 'cs/compare.html'
    title = 'Сравнение концепций'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        concepts = ComputerScienceConcept.published.all()
        context['concepts'] = concepts

        concept1_slug = self.request.GET.get('concept1')
        concept2_slug = self.request.GET.get('concept2')

        context['concept1_slug'] = concept1_slug
        context['concept2_slug'] = concept2_slug

        concept1 = None
        concept2 = None

        if concept1_slug:
            try:
                concept1 = ComputerScienceConcept.published.get(slug=concept1_slug)
            except ComputerScienceConcept.DoesNotExist:
                pass
        if concept2_slug:
            try:
                concept2 = ComputerScienceConcept.published.get(slug=concept2_slug)
            except ComputerScienceConcept.DoesNotExist:
                pass

        context['concept1'] = concept1
        context['concept2'] = concept2

        return context


class ConceptByTagListView(DataMixin, ListView):
    model = ComputerScienceConcept
    template_name = 'cs/concepts_by_tag.html'
    context_object_name = 'concepts'
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        return ComputerScienceConcept.published.filter(tags__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        tag = Tag.objects.get(slug=tag_slug)
        context['title'] = f"Концепции по тегу: {tag.name}"
        context['tag'] = tag
        return context