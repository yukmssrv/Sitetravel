from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Country, TagPost, Category
from django.shortcuts import get_object_or_404
from .forms import AddPostForm, UploadFileForm
import uuid
import os
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import DataMixin

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]
posts_db = [
    {
        'id': 1,
        'title': 'Россия',
        'content': 'Россия — самая большая страна в мире, известная своими природными богатствами.',
        'is_published': True,
        'cat_id': 2,   # Природа
    },
    {
        'id': 2,
        'title': 'Италия',
        'content': 'Италия славится своей кухней, историей и архитектурой.',
        'is_published': True,
        'cat_id': 1,   # Архитектура
    },
    {
        'id': 3,
        'title': 'Франция',
        'content': 'Франция — страна романтики, моды и изысканной кухни.',
        'is_published': True,
        'cat_id': 3,   # Музеи
    },
]
def cities_by_country(request, country_slug):
    allowed_countries = ['russia', 'italy', 'china', 'france', 'japan']
    if country_slug.lower() not in allowed_countries:
        raise Http404("Страна не найдена")
    return HttpResponse(f"<h1>Города страны: {country_slug}</h1>")

def archive(request, year):
    return HttpResponse(f"<h1>Архив путешествий за {year} год</h1>")

def old_countries_redirect(request):
    return redirect('destinations_list', permanent=True)

def some_view(request):
    url = reverse('country_detail', args=[7])
    return HttpResponse(f"Ссылка на страну: {url}")

def countries_list(request):
    sort = request.GET.get('sort', 'name')
    return render(request, 'country/countries_list.html', {'sort': sort, 'menu': menu})

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена (404)</h1><p>Попробуйте другой адрес.</p>")

class HomeView(DataMixin, ListView):
    model = Country
    template_name = 'country/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Country.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, cat_selected=0)

def handle_uploaded_file(f):
    # Генерируем уникальное имя
    name, ext = os.path.splitext(f.name)
    if not ext:
        ext = ''
    unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
    with open(f"uploads/{unique_name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return unique_name

class AboutView(DataMixin, View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'country/about.html', {'form': form, 'menu': menu, 'title': 'О сайте'})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
            return redirect('about')
        return render(request, 'country/about.html', {'form': form, 'menu': menu, 'title': 'О сайте'})

class ContactView(DataMixin, TemplateView):
    template_name = 'country/contact.html'
    title_page = 'Обратная связь'

class LoginView(DataMixin, TemplateView):
    template_name = 'country/login.html'
    title_page = 'Вход'


class CountryDetailView(DataMixin, DetailView):
    model = Country
    template_name = 'country/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_queryset(self):
        return Country.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


cats_db = [
    {'id': 1, 'name': 'Архитектура'},
    {'id': 2, 'name': 'Природа'},
    {'id': 3, 'name': 'Музеи'},
]

class CategoryListView(DataMixin, ListView):
    model = Country
    template_name = 'country/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Country.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug=self.kwargs['cat_slug'])
        return self.get_mixin_context(context, title=f'Категория: {cat.name}', cat_selected=cat.pk)


class TagListView(DataMixin, ListView):
    model = Country
    template_name = 'country/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Country.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')


class CountryCreateView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'country/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление страны'

class AddPage(DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'country/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление страны'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CountryUpdateView(DataMixin, UpdateView):
    model = Country
    form_class = AddPostForm
    template_name = 'country/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование страны'

class CountryDeleteView(DataMixin, DeleteView):
    model = Country
    success_url = reverse_lazy('home')
    template_name = 'country/delete_confirm.html'
    title_page = 'Удаление страны'






