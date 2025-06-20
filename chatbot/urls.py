from django.urls import path
from .views import chat_api

app_name = 'chatbot'

urlpatterns = [
    # this will match POST /en/chatbot/api/chat/ (or whatever your language prefix is)
    path('', chat_api, name='chat_api'),
]
