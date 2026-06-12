from django.urls import path, register_converter
from . import converters, views
from django.views.generic.base import RedirectView

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    # Главные страницы
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    #Каталог стран и сортировка
    path('countries/', views.countries_list, name='countries'),
    path('destinations/', views.countries_list, name='destinations_list'),
    # Категории и теги
    path('category/<slug:cat_slug>/', views.CategoryListView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagListView.as_view(), name='tag'),
    # Детальный просмотр
    path('post/<slug:post_slug>/', views.CountryDetailView.as_view(), name='post'),
    path('attraction/<slug:attraction_slug>/', views.AttractionDetailView.as_view(), name='attraction'),
    # CRUD операции
    path('add/', views.CountryCreateView.as_view(), name='add_page'),
    path('edit/<int:pk>/', views.CountryUpdateView.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.CountryDeleteView.as_view(), name='delete_page'),
    # Комментарии и лайки
    path('post/<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:post_slug>/like/', views.toggle_like, name='toggle_like'),
    # Дополнительные эксперименты
    path('countries/<slug:country_slug>/cities/', views.cities_by_country, name='cities'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('countries/', RedirectView.as_view(pattern_name='destinations_list', permanent=False)),
    path('test-reverse/', views.some_view, name='test_reverse'),
    path('old-countries/', views.old_countries_redirect, name='old_countries'),
]
