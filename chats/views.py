from django.views.generic import DetailView
from .models import Chat


class ChatDetailView(DetailView):
    model = Chat
    template_name = "chat_detail.html"
    context_object_name = "chat"
