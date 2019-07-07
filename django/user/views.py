from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from user.forms import ActualUserCreationForm, UserLoginForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
import re


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = ActualUserCreationForm
    success_url = reverse_lazy('core:MovieList')


class LoginView(View):
    def post(self, request):
        form = UserLoginForm(request.POST)
        message = '请检查填写的内容！'
        if form.is_valid():
            username = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            # 如果符合邮件正则
            if re.match(r'^[0-9a-zA-Z_.]+@[A-Za-z]+\.[a-zA-Z]+$', str(username)):
                email = username
                try:
                    email_user = User.objects.get(email=email)
                except User.DoesNotExist:
                    message = '邮件不存在'
                    return render(request, 'registration/login.html', {'form': form, 'message': message})
                if email_user is not None:
                    username = email_user.username

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('core:MovieList'))

        return render(request, 'registration/login.html', {'form': form, 'message': message})

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'registration/login.html', {'form': form})
