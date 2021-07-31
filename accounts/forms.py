from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import User, VerifyCode


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'password', 'phone', 'first_name', 'last_name', 'email', 'national_code',
            'date_of_birth', 'is_active', 'is_admin'
        )


class LoginRegisterForm(forms.Form):
    phone_or_email = forms.CharField(
        max_length=200, label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone or email'})
    )


class VerifyForm(forms.ModelForm):
    code = forms.CharField(
        max_length=6, label='Code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'verify code'}),
        help_text='Enter SMS verification code'
    )

    class Meta:
        model = VerifyCode
        fields = ('code',)


class LoginByPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'})
    )


class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'national_code', 'date_of_birth')


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'new password'})
    )

    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm new password'})
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class EditPasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'current password'})
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'new password'})
    )

    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm new password'})
    )

    def clean_new_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class EditPhoneForm(forms.Form):
    new_phone = forms.CharField(
        max_length=11, label='new phone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'new phone'}),
        validators=[
            RegexValidator(
                regex='09(0[1-2]|1[0-9]|3[0-9]|2[0-1])-?[0-9]{3}-?[0-9]{4}',
                message="Phone number must be entered in the format: '91212345678'."
            ),
        ]
    )

