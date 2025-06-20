from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.forms import CustomUserForm  # if you have a custom form, or skip this line
from users.views import CustomRegistrationView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from chatbot.views import chat_api




urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('chat_api/', chat_api, name='chat_api'),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('auth.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('posts.urls', namespace='posts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('profile/', include('users.urls', namespace='profile')),
    path('products/', include('products.urls', namespace='products')),
    path('', include('pages.urls', namespace='pages')),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/complete/', TemplateView.as_view(template_name='registration_complete.html'), name='django_registration_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/register/', CustomRegistrationView.as_view(), name='django_registration_register'),
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),

)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
