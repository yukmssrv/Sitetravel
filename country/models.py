from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Country.Status.PUBLISHED)
class Country(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED, verbose_name="Опубликовано")

    objects = models.Manager()
    published = PublishedManager()

    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='countries')
    extrainfo = models.OneToOneField('ExtraInfo', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='country_extrainfo')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name="Изображение")

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
        ]
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post', kwargs={'post_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class ExtraInfo(models.Model):
    capital = models.CharField(max_length=100, blank=True, verbose_name="Столица")
    population = models.IntegerField(null=True, blank=True, verbose_name="Население")

    def __str__(self):
        return f"Доп. инфо: {self.capital}, население {self.population}"

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'

