from django.urls import path

from chats import views

app_name = "chats"

urlpatterns = [
    path("<int:pk>/", views.ChatDetailView.as_view(), name="chat_detail"),
    path("create_chat/", views.ChatCreateView.as_view(), name="chat_create"),
]