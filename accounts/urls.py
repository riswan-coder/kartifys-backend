from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, ProfileView, LogoutView,
    UserListView, UserUpdateView,
    ForgotPasswordView, ResetPasswordView,
    SendOTPView, VerifyOTPView, ResetPasswordWithOTPView,
    AdminUpdateUserPasswordView, ChangeOwnPasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserUpdateView.as_view()),
    path('users/<int:pk>/set-password/', AdminUpdateUserPasswordView.as_view()),
    path('change-password/', ChangeOwnPasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('reset-password-otp/', ResetPasswordWithOTPView.as_view()),
]