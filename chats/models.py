from django.db import models
# from users.models import MyUser
from django.conf import settings


class Chat(models.Model):
    creator = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name="chats_created")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of chat creation")
    members = models.ManyToManyField("users.MyUser", related_name="chats_member")

    def __str__(self):
        return f"Created by {self.creator} at: {self.created_at}"

    class Meta:
        verbose_name_plural = "Chats"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("users.MyUser", on_delete=models.CASCADE, related_name="messages_sent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of message sent")
    text = models.TextField(verbose_name="message text")

    def __str__(self):
        return f"Sent by {self.sender} at: {self.created_at} with text: {self.text}. Chat is {self.chat}"

    class Meta:
        verbose_name_plural = "Messages"
