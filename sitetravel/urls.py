from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from country import views
from django.contrib import admin


admin.site.site_header = "Панель администрирования сайта о путешествиях"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Добро пожаловать в панель управления"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('country.urls')),
    path('users/', include('users.urls', namespace='users')),

]

handler404 = 'country.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)