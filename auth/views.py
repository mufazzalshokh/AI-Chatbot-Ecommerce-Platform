from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def password_changed(request):
    messages.add_message(request, messages.INFO, 'Password changed successfully')
    return redirect(reverse('profile:home'))


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
