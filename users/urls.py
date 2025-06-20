from django.urls import path, include



from users.views import ProfileUpdateView
from users.views import CustomRegistrationView


app_name = 'profile'

urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='home'),
    path('accounts/register/', CustomRegistrationView.as_view(), name='django_registration_register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
