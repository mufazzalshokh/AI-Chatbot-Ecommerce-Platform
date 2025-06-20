from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django_registration.views import RegistrationView
from django.urls import reverse


from users.forms import ProfileModelForm
from users.models import ProfileModel
from .forms import CustomUserForm



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileModelForm
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        profile, _ = ProfileModel.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse('profile:home')




class CustomRegistrationView(RegistrationView):
    form_class = CustomUserForm
    template_name = 'registration/registration_form.html'

    def register(self, form):
        new_user = form.save()
        login(self.request, new_user)  # log in the user manually
        return new_user

    def get_success_url(self, request, user=None):
            print(">>> redirecting to home")  # ADD THIS
            return '/'
