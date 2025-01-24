# Import necessary modules and classes
import threading
from collections.abc import Mapping
from typing import Any
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm ,
   
   
)
from django.forms.utils import ErrorList
# Get the user model for the Django application
User = get_user_model()

# User Login Form
class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the HTML class attribute for each field's widget to "form-control"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # Username field
    username = forms.CharField(
        max_length=150,
    )
    
    # Password field
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    # Additional password field with a password input widget
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the HTML class attribute for each field's widget to "form-control"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        # Define the model and fields for the form
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    # Validate that the username is unique
    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model

        # Check if a user with the same username already exists
        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("User with the username already exists")
        return username

    # Validate that the email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model

        # Check if a user with the same email already exists
        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User with the Email already exists")
        return email

    # Validate that the password and password confirmation match
    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.data.get('password2')

        # Check if passwords match
        if password != password2:
            raise forms.ValidationError("Password mismatch")

        return password

    # Save the user instance with the hashed password
    def save(self, commit=True, *args, **kwargs):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))

        # Save the user to the database if commit is True
        if commit:
            user.save()

        return user


class ChangePasswordForm(forms.Form):
    # Additional password field with a password input widget
    current_password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )    
    new_password1 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )    
    new_password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

    def __init__(self,user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # Set the HTML class attribute for each field's widget to "form-control"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean_current_password(self, *args, **kwargs):
        current_password = self.cleaned_data.get('current_password')

        # Check if passwords match
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current Password Incorrect")

        return current_password
    # Validate that the password and password confirmation match
    def clean_new_password1(self, *args, **kwargs):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.data.get('new_password2')

        # Check if passwords match
        if new_password1 != new_password2:
            raise forms.ValidationError("Password mismatch")

        return new_password1

#============For send Email=======================

class SendEmailForm(PasswordResetForm,threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        threading.Thread.__init__(self)
    # Set the HTML class attribute for each field's widget to "form-control"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        if not User.objects.filter(email__iexact=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("The Email is not registered")
        
        return self.cleaned_data.get('email')
    
    def run(self) -> None:
        return super().send_mail(
        self.subject_template_name,
        self.email_template_name,
        self.context,
        self.from_email,
        self.to_email,
        self.html_email_template_name,
        )
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name):
        self.subject_template_name = subject_template_name
        self.email_template_name = email_template_name
        self.context = context
        self.from_email = from_email
        self.to_email = to_email
        self.html_email_template_name = html_email_template_name
        self.start()



class ResetPasswordConfirmForm(forms.Form):  
    new_password1 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )    
    new_password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

    def __init__(self,user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # Set the HTML class attribute for each field's widget to "form-control"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    
    # Validate that the password and password confirmation match
    def clean_new_password1(self, *args, **kwargs):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.data.get('new_password2')

        # Check if passwords match
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Password mismatch")

        return new_password1


        # Save the user instance with the hashed password
    def save(self, commit=True, *args, **kwargs):
        
        self.user.set_password(self.cleaned_data.get('new_password1'))

        # Save the user to the database if commit is True
        if commit:
            self.user.save()

        return self.user