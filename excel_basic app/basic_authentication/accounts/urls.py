from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('otp-login/', views.otp_login_view, name='otp_login'),
    path('home/', views.home_view, name='home'),
]
