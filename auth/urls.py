from django.urls import path, include
from .views import RegisterView

from auth.views import password_changed

urlpatterns = [
    path('password/change/done', password_changed),
    path('', include('django_registration.backends.activation.urls')),
    path('', include('django.contrib.auth.urls')),  # for login/logout/password reset
    path('register/', RegisterView.as_view(), name='registration_register'),

]
