from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0009_alter_category_options_alter_country_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.FileField(blank=True, null=True, upload_to='attractions/%Y/%m/%d/', verbose_name='Фото')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attractions', to='country.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Достопримечательность',
                'verbose_name_plural': 'Достопримечательности',
                'ordering': ['title'],
            },
        ),
    ]
