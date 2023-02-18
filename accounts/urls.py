from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup_user"),
    path("login/", Login.as_view(), name="login_user"),
    path("logout/", Logout.as_view(), name="logout_user"),
    path("profile/", Profile.as_view(), name="profile_user"),
]
