from django.urls import path
from .views import (
    SavedProfile,
    RegisterView,
    LoginView,
    LogoutView,
    MainProfile,
    PostsProfile,
    CommentsProfile,
    UpvotedProfile,
    DownvotedProfile,
    ProfileSettings,
)

app_name = "accounts"
urlpatterns = [
    # AUTH
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView, name="logout"),
    # PROFILE
    path("user/<slug:username>/", MainProfile, name="profile-overview"),
    path("settings/profile/", ProfileSettings.as_view(), name="profile-settings"),
    path("user/<slug:username>/posts/", PostsProfile, name="profile-posts"),
    path("user/<slug:username>/comments/", CommentsProfile, name="profile-comments"),
    path("user/<slug:username>/upvoted/", UpvotedProfile, name="profile-upvoted"),
    path("user/<slug:username>/downvoted/", DownvotedProfile, name="profile-downvoted"),
    path("user/<slug:username>/saved/", SavedProfile, name="profile-saved"),
]
