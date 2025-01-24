
from django.urls import path
from django.contrib.auth.views import(
   
    PasswordResetDoneView,
    

)
from . views import (
  
    LoginView,
    LogoutView,
    RegistrationView,
    ChangePasswordView,
    SendEmailToResetPassword,
    ResetPasswordConfirmView,
    # ActivationView,
)
urlpatterns = [
 
    path('',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('registration/',RegistrationView.as_view(),name="registration"),
    # path('activate/<uidb64>/<token>/',ActivationView.as_view(),name='activate'),
    path('change_password/',ChangePasswordView.as_view(),name="change_password"),
    path('password_reset/',SendEmailToResetPassword.as_view(),name="password_reset"),
    path('password_reset/done/',PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',ResetPasswordConfirmView.as_view(),name="password_reset_confirm"),

    
]
"""
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""