from django.urls import path

from chats.views import ChatDetailView

urlpatterns = [
    path("<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
]