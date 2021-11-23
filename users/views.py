import os
import requests

from django.views import View
from django.views.generic import FormView

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

from . import forms as user_forms
from . import models as user_models


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


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = user_forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {  # 폼에 들어갈 기본 데이터를 미리 입력
        "first_name": "Nicoas",
        "last_name": "Serr",
        "email": "hosibito@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()  # 모델안의 이메일 보내는 함수 호출
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add succes message
    except user_models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    # print(request.GET)
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # print(token_request.json())
            # {'access_token': 'gho_WXdmTQ8N...', 'token_type': 'bearer', 'scope': 'read:user'}
            token_json = token_request.json()
            error = token_json.get("error", None)

            if error is not None:
                print("깃허브에서 토큰을 받아오면서 오류가 생겼다")
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                api_request = requests.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}"},
                )
                # print(api_request.json())
                # 17 LOG IN WITH GITHUB access_token 으로 user를 받아온다. 확인
                profile_json = api_request.json()  # 유저를 깃허브에서 받아오는데 성공!
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name", None)
                    email = profile_json.get("email", None)

                    if email is None:
                        # 깃허브에서 이메일정보를 못가져온다. 오류처리할것
                        print("깃허브에서 이메일정보를 못가져온다.")
                        raise GithubException()

                    bio = profile_json.get("bio", None)
                    if bio is None:
                        bio = ""

                    try:
                        user = user_models.User.objects.get(email=email)
                        # 이미 로그인해 있거나. 가입해있는유저
                        if user.login_method != user_models.User.LOGIN_GITHUB:
                            # 다른방식으로 가입해 있는 유저
                            print("깃허브가 아닌 다른방식으로 가입해 있는 유저")
                            raise GithubException()
                    except user_models.User.DoesNotExist:
                        # 새로 가입해야할 유저
                        user = user_models.User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            email_verified=True,
                            login_method=user_models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()  # 깃허브로 가입하는 유저이므로 패스워드가 필요없다
                        user.save()

                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # 에러메시지 포함시킬것
        return redirect(reverse("users:login"))
