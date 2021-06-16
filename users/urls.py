from django.urls import path

from users.views import UserDetailView

app_name = "users"

urlpatterns = [
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]