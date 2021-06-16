from django.views.generic import DetailView
from django.core import serializers
from .models import Chat


class ChatDetailView(DetailView):
    model = Chat
    template_name = "chat_detail.html"
    context_object_name = "chat"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["chat"] = serializers.serialize("json", Chat.objects.filter(pk=self.kwargs["pk"]))
        return context
