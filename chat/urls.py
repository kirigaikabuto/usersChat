from django.urls import path
from .views import *
urlpatterns = [
    path("chat/", chat_page, name="chat_page")
]
