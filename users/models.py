from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo = models.FileField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'



