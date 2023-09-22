from django.urls import path

from .views import SignupView, LoginView, FollowUserView
# from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("<str:user>/follow", FollowUserView.as_view()),
]



