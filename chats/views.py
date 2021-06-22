from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.core import serializers

from .forms import ChatCreateForm
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


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ["members", ]
    template_name  = "chat_create.html"

    def get(self, request, *args, **kwargs):
        """
        Override for moderate queryset output in rendered form
        """
        form = ChatCreateForm()
        form.fields["members"].queryset = form.fields["members"].queryset.exclude(
            pk=self.request.user.pk
        )
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        super().form_valid(form)

        chat = Chat.objects.get(pk=form.instance.pk)
        chat.members.add(self.request.user.pk)

        return HttpResponseRedirect(self.get_success_url())

    # Alternative realization
    # def form_valid(self, form):
    #     new_chat_bounded_form = form.save(commit=False)
    #     new_chat_bounded_form.creator = self.request.user
    #     super().form_valid(form)
    #
    #     chat = Chat.objects.get(pk=form.instance.pk)
    #     chat.members.add(self.request.user.pk)
    #     return HttpResponseRedirect(self.get_success_url())
