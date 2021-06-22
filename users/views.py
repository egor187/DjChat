from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from users.models import MyUser


class UserDetailView(LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = 'user_detail.html'
    context_object_name = "user"
