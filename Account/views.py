# Import necessary Django modules and classes
from typing import Any
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import LogoutRequiredMixin  # Assuming this is a custom mixin
from django.urls import reverse_lazy
from .forms import(
     LoginForm, 
     UserRegistrationForm,
     ChangePasswordForm,
     SendEmailForm,
     ResetPasswordConfirmForm,
)
from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetConfirmView,
   
)
#========================
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string

# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#========================
# Create your views here.

# # Home View - Requires Login
# @method_decorator(never_cache, name='dispatch')
# class HomeView(LoginRequiredMixin, generic.TemplateView):
#     login_url = 'login'
#     template_name = "account/home.html"

# User Login View
@method_decorator(never_cache, name='dispatch')
class LoginView(LogoutRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {"form": form}
        return render(self.request, 'account/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            user = authenticate(
                self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                login(self.request, user)
                return redirect('home')  # Redirect to the home page upon successful login
            else:
                messages.warning(self.request, "Wrong credentials")
                return redirect('login')
        context = {"form": form}
        return render(self.request, 'account/login.html', context)

# User Logout View
class LogoutView(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')  # Redirect to the login page after logout

# User Registration View
@method_decorator(never_cache, name='dispatch')
class RegistrationView(LogoutRequiredMixin, generic.CreateView):
    template_name = "account/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')  # Redirect to the login page upon successful registration

    def form_valid(self, form):
        messages.success(self.request, "Registration Successful!")
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class ChangePasswordView(LoginRequiredMixin, generic.FormView):
    template_name = "account/change_password.html"
    form_class = ChangePasswordForm 
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('login')  # Redirect to the login page upon successful registration

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['user']= self.request.user
        return context
    
    def form_valid(self, form):
        #password hash 
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password1'))
        user.save()
        messages.success(self.request, "Password changed Successful!")
        return super().form_valid(form)
    


#================For sending Email=================
class SendEmailToResetPassword(PasswordResetView):
    template_name = 'account/password_reset.html'
    # from forms.py file 
    form_class=SendEmailForm


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    form_class=ResetPasswordConfirmForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,"Password reset successfully")
        return super().form_valid(form)
    
