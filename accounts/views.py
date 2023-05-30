from django.shortcuts import render, redirect
from allauth.account import views


# ログイン
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

# ログアウト
class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

# サインアップ
class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
