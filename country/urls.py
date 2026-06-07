from django.urls import path, register_converter
from . import converters, views
from django.views.generic.base import RedirectView

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('countries/', views.countries_list, name='countries'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    #path('login/', views.LoginView.as_view(), name='login'),
    path('category/<slug:cat_slug>/', views.CategoryListView.as_view(), name='category'),
    path('countries/<slug:country_slug>/cities/', views.cities_by_country, name='cities'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('destinations/', views.countries_list, name='destinations_list'),
    path('countries/', RedirectView.as_view(pattern_name='destinations_list', permanent=False)),
    path('test-reverse/', views.some_view, name='test_reverse'),
    path('old-countries/', views.old_countries_redirect, name='old_countries'),
    path('post/<slug:post_slug>/', views.CountryDetailView.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', views.TagListView.as_view(), name='tag'),
    #path('add/', views.AddPage.as_view(), name='add_page'),
    path('add/', views.CountryCreateView.as_view(), name='add_page'),
    path('edit/<int:pk>/', views.CountryUpdateView.as_view(), name='edit_page'),
    path('delete/<int:pk>/', views.CountryDeleteView.as_view(), name='delete_page'),
]