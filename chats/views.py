from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.core import serializers

from .forms import ChatCreateForm
from .models import Chat, Message


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chat_detail.html"
    context_object_name = "chat"
    access_denied_msg = "You are not member of this chat"

    def dispatch(self, request, *args, **kwargs):
        """
        Protect for getting access to chat_page from "not-members" of that chat
        """
        if self.kwargs["pk"] not in self.request.user.get_chats_membership().values_list("pk", flat=True):
            messages.error(request, self.access_denied_msg)
            return redirect(reverse_lazy("index"))
        else:
            return super().dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["chat_pk"] = Chat.objects.get(pk=self.kwargs["pk"]).pk

        # context["all_messages"] = serializers.serialize("json", Message.objects.filter(chat=self.object), fields="text")
        # context["all"] = Message.objects.filter(chat=self.object).values_list("text", flat=True)

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


class ChatDeleteView(DeleteView):
    model = Chat
    template_name = "chat_delete.html"
    success_url = reverse_lazy("index")
