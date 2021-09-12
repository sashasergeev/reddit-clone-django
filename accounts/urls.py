from django.urls import path, include
from .views import (
    register,
    LoginView,
    LogoutView,
    MainProfile,
    PostsProfile,
    CommentsProfile,
    UpvotedProfile,
    DownvotedProfile,
    ProfileSettings
)

app_name = "accounts"
urlpatterns = [
    # AUTH
    path("accounts/login/", LoginView, name="login"),
    path("accounts/register/", register, name="register"),
    path("accounts/logout/", LogoutView, name="logout"),
    # PROFILE
    path("user/<slug:username>/", MainProfile, name="profile-overview"),
    path("settings/profile/", ProfileSettings, name="profile-settings"),
    path("user/<slug:username>/posts/", PostsProfile, name="profile-posts"),
    path("user/<slug:username>/comments/", CommentsProfile, name="profile-comments"),
    path("user/<slug:username>/upvoted/", UpvotedProfile, name="profile-upvoted"),
    path("user/<slug:username>/downvoted/", DownvotedProfile, name="profile-downvoted"),
]
