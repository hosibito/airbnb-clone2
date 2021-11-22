from django.views import View
from django.views.generic import FormView

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

from . import forms as user_forms


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = user_forms.LoginForm  # () 없음에 주의
    success_url = reverse_lazy("core:home")  # url을 부를때 생성

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # get post is_valid 다 필요없다.. 다만.. 이해하기 힘들기도 하다.
    # LoginView 도 있으나 기능이 너무 많다. (유저네임을 강제하기도 하고)
    # 로그인은 이와같이 FormView를 이용하는것을 추천..
    # 개념정리 꼭 확인할것!!! 그냥 이걸보면.. 너무. 간략화되어 이해하기 힘들다.


class LoginView_old(View):
    def get(self, request):
        form = user_forms.LoginForm(initial={"email": "test@test.com"})  # 기본값
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = user_forms.LoginForm(request.POST)  # 입력된값 저장. bounced form
        # print(form.is_valid())  # True
        if form.is_valid():
            # print(form.cleaned_data)  # {'email': 'lalalalal', 'password': 'lalala'}
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


"""
14.4 확인할것.
"""
