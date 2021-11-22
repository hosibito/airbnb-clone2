from django.views import View
from django.shortcuts import render

from . import forms as user_forms


class LoginView(View):
    def get(self, request):
        form = user_forms.LoginForm(initial={"email": "test@test.com"})  # 기본값
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = user_forms.LoginForm(request.POST)  # 입력된값 저장. bounced form
        # print(form)
        print(form.is_valid())  # True
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})


def login_view(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
