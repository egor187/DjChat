from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("register/", views.UserRegisterView.as_view(), name="user_registration"),
]