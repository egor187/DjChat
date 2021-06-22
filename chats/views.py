from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core import serializers

from .models import Chat, Message


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chat_detail.html"
    context_object_name = "chat"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["chat_pk"] = Chat.objects.get(pk=self.kwargs["pk"]).pk

        # context["all_messages"] = serializers.serialize("json", Message.objects.filter(chat=self.object), fields="text")
        context["all"] = Message.objects.filter(chat=self.object).values_list("text", flat=True)

        return context
