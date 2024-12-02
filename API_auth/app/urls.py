from django.urls import path
from .views import AuthRequestView, VerifyProfileView, ProfileView, ActInvaiteCodeView 

urlpatterns = [
    path('auth/request-code/', AuthRequestView.as_view(), name='auth-request-code'),
    path('auth/verify-code/', VerifyProfileView.as_view(), name='verify-code'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate-invite-code/', ActInvaiteCodeView.as_view(), name='activate-invite-code'),
]