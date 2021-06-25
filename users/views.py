from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView

from users.forms import UserCreationForm
from users.models import MyUser


class UserDetailView(LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = 'user_detail.html'
    context_object_name = "user"


class UserRegisterView(CreateView):
    model = MyUser
    form_class = UserCreationForm
    template_name = 'registration/user_register.html'
    context_object_name = "user"

    def get_success_url(self):
        login(self.request, user=self.object)
        return super().get_success_url()
