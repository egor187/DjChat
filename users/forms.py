from django.contrib.auth import forms

from users.models import MyUser

class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = MyUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


