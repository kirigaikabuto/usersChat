from django.urls import path
from .views import *
urlpatterns = [
    path("chat/<int:user2_pk>/", chat_page, name="chat_page")
]
