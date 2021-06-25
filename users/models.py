from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from chats.models import Chat


class MyUser(AbstractUser):
    def get_chats_created(self):
        """
        :return: queryset of 'Chat' instances in which 'self' user related like 'creator'
        """
        chats = Chat.objects.filter(creator=self)
        return chats

    def get_chats_membership(self):
        """
        :return: queryset of 'Chat' instances in which 'self' user related like 'member'
        """
        chats = Chat.objects.filter(members=self)
        return chats

    def get_absolute_url(self):
        return reverse_lazy('users:user_detail', args=[self.pk])

