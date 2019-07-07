from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput


class ActualUserCreationForm(UserCreationForm):
    username = forms.CharField(label="用户名", max_length=256,
                               widget=forms.TextInput(
                                   attrs={"placeholder": "username/email", 'autofocus': '', 'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
    password2 = forms.CharField(label="重复密码", max_length=256,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'password again', 'class': 'form-control'}))

    email = forms.CharField(label="email", max_length=256,
                            widget=forms.EmailInput(attrs={"placeholder": "user@gmail.com", 'class': 'form-control'}))
    genders = (('male', "男"), ('famale', '女'))
    gender = forms.ChoiceField(label="性别", choices=genders)

    # captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={'placeholder': '验证码', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label="用户名或e-mail", max_length=256,
                                        widget=forms.TextInput(
                                            attrs={"placeholder": "username/email", 'autofocus': '',
                                                   'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
    # captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={'placeholder': '验证码', 'class': 'form-control'}))


