from accounts.views import ChangeProfilePicView, GetProfilePicView, UserRegistrationView,UserLoginView,AllUserView,TokenBasedView
from django.urls import path


urlpatterns=[
path('register/', UserRegistrationView.as_view(), name='register'),
path('login/', UserLoginView.as_view(), name='login'),
path('allUsers/', AllUserView.as_view(), name='alluser'),
path('profilePic/',ChangeProfilePicView.as_view(), name='profile pic' ),
path('seeProfilePic/',GetProfilePicView.as_view(), name='see profile pic' ),
path('token/me/',TokenBasedView.as_view(), name='token based details' ),




]