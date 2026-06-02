from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.chatbot_api_view, name='chatbot_api'),
]
