from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from .forms import ProfileUserForm
from django.contrib.auth.views import PasswordChangeView
from .forms import UserPasswordChangeForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from .forms import UserProfileForm
from .models import UserProfile
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин или E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_user_profile(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileForm(instance=self.get_user_profile())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = UserProfileForm(request.POST, request.FILES, instance=self.get_user_profile())
        if form.is_valid() and profile_form.is_valid():
            if request.FILES.get('photo'):
                profile_form.save()
            return self.form_valid(form)
        context = self.get_context_data(form=form)
        context['profile_form'] = profile_form
        return self.render_to_response(context)


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}
