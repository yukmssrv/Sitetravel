from django import forms
from .models import Country, Category
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Выберите категорию")

    class Meta:
        model = Country
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError('Название должно быть не короче 3 символов')
        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Выберите файл")
