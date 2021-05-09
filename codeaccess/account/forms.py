"""form class defining here.."""
from django.forms import ModelForm
from django import forms
from .models import User


class Registration(ModelForm):
    """User registraion form .."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': "email_or_phone", 'class': "form-label-group form-control "}))
    password2 = forms.CharField(label='conform password', widget=forms.PasswordInput(attrs={'placeholder': "email_or_phone", 'class': "form-label-group form-control "}))

    class Meta:
        """docstring for ClassName.."""

        model = User
        fields = {'username'}
        widgets = {"username": forms.TextInput(attrs={'placeholder': "email_or_phone", 'class': "form-label-group form-control "})}
        labels = {"username": "email_or_phone"}

    def clean_password2(self):
        """Check that the two password entries match.."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format.."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        email_or_phone = self.cleaned_data['username']

        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            # email_or_phone = self.normalize_email(email_or_phone)
            user.email, user.mobile = email_or_phone, ""
        else:

            user.email, user.mobile = "", email_or_phone

        if commit:

            user.save()

        return user


class OTP(forms.Form):
    """class for otp validation.."""

    otp_input = forms.CharField(label='ENTER OTP', widget=forms.TextInput(attrs={'placeholder': "ENTER OTP", 'class': "form-label-group form-control "}))


class Login(forms.Form):
    """user  for Login form .."""

    user_name = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': "ENTER OTP", 'class': "form-label-group form-control "}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': "ENTER OTP", 'class': "form-label-group form-control "}))


class PasswordReset(forms.Form):
    """reset password form ..."""

    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': "ENTER OTP", 'class': "form-label-group form-control "}))


class PasswordSet(forms.Form):
    """docstring for ClassName.."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': "email_or_phone", 'class': "form-label-group form-control "}))
    password2 = forms.CharField(label='conform password', widget=forms.PasswordInput(attrs={'placeholder': "email_or_phone", 'class': "form-label-group form-control "}))

    def clean_password2(self):
        """Check that the two password entries match.."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
