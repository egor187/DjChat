from django.shortcuts import render
from django.views.generic import DetailView
from users.models import MyUser


class UserDetailView(DetailView):
    model = MyUser
    template_name = 'user_detail.html'
    context_object_name = "user"
