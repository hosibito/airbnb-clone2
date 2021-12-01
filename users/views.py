import os
import requests

from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from . import forms as user_forms
from . import models as user_models
from . import mixins as user_mixins


class LoginView(user_mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = user_forms.LoginForm  # () 없음에 주의

    # success_url = reverse_lazy("core:home")  # url을 부를때 생성
    def get_success_url(self):  # ?next=/users/update-profile/ 처리 21.9 참고
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

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


def log_out(request):
    messages.info(request, f"{request.user.username}님 로그아웃 하셧습니다.  ")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(user_mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = user_forms.SignUpForm
    success_url = reverse_lazy("core:home")

    # initial = {  # 폼에 들어갈 기본 데이터를 미리 입력
    #     "first_name": "Nicoas",
    #     "last_name": "Serr",
    #     "email": "itn@las.com",
    # }

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        # print(user)
        if user is not None:
            user.email = username
            user.save()
            login(self.request, user)

        user.verify_email()  # 모델안의 이메일 보내는 함수 호출
        return super().form_valid(form)
        """
        아마도!!
        form.save() 가 폼을 기반으로 이미 유저를 만드는게 아닌가 싶다.
        그러니 form이 email 이었을때 username가 비어있는 유저가 생성된게 설명됨..
        그러고 유저명으로 검색하니 None 이넘어오고 메일이 안보내진다..

        좀더 파고들어볼것.. 유저가 없으면 만들어서. user.verify_email() 보내고 있다...
        다만 만드는게 좀 이상하다.. form 입력된걸 기반으로 만들어서. 다시 돌린다는 느낌이다.
        """


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
                f"https://github.com/login/oauth/access_token?client_id={client_id}\
                    &client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # print(token_request.json())
            # {'access_token': 'gho_WXdmTQ8N...', 'token_type': 'bearer', 'scope': 'read:user'}
            token_json = token_request.json()
            error = token_json.get("error", None)

            if error is not None:
                raise GithubException(f"깃허브 토큰을 받아오며 오류가 생겼습니다 error : {error}")
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
                        raise GithubException("깃허브 유저 정보에 email이 없습니다. ")

                    bio = profile_json.get("bio", None)
                    if bio is None:
                        bio = ""

                    try:
                        user = user_models.User.objects.get(email=email)
                        # 이미 로그인해 있거나. 가입해있는유저
                        if user.login_method != user_models.User.LOGIN_GITHUB:
                            # 다른방식으로 가입해 있는 유저
                            raise GithubException(f"{user.login_method}로 로그인해 주세요.")
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
                    messages.success(request, f"환영합니다. {user.username}님")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("깃허브 유저 정보를 가져오지 못했습니다. ")
        else:
            raise GithubException("깃허브 에서 code를 받아오지 못했습니다. ")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
    REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}\
            &redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    # print(request.GET)  # <QueryDict: {'code': ['61WpYAVoPFXBq...']}>
    try:
        code = request.GET.get("code")
        REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
        if code is not None:
            token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": REST_API_KEY,
                    "redirect_uri": REDIRECT_URI,
                    "code": code,
                },
            )
            # token_request = requests.get(
            #     f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
            # )
            token_json = token_request.json()
            # print(token_json)  # {'access_token': 'I6l9m....', .....
            error = token_json.get("error", None)
            if error is not None:
                raise KakaoException(f"카카오 토큰을 얻어오면서 에러 발생 error:{error}")
            else:
                access_token = token_json.get("access_token")
                api_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                # print(api_request.json())
                profile_json = api_request.json()
                # print(profile_json)
                id = profile_json.get("id")
                if id is not None:
                    email = profile_json.get("kakao_account").get("email", None)
                    properties = profile_json.get("properties")
                    nickname = properties.get("nickname")
                    profile_image = properties.get("profile_image")

                    if email is None:
                        # 카카오에서 이메일정보를 못가져온다. 오류처리할것
                        raise KakaoException("카카오에서 이메일정보를 제공하지 않습니다.")

                    try:
                        user = user_models.User.objects.get(email=email)
                        # 이미 로그인해 있거나. 가입해있는유저
                        if user.login_method != user_models.User.LOGING_KAKAO:
                            # 다른방식으로 가입해 있는 유저
                            raise KakaoException(f"{user.login_method}로 로그인해 주세요.")
                    except user_models.User.DoesNotExist:
                        # 새로 가입해야할 유저
                        user = user_models.User.objects.create(
                            username=email,
                            first_name=nickname,
                            bio="",
                            email=email,
                            email_verified=True,
                            login_method=user_models.User.LOGING_KAKAO,
                        )
                        user.set_unusable_password()
                        user.save()

                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{nickname}-avatar", ContentFile(photo_request.content)
                            )
                            # 이미지 파일이면 그나름대로 처리하는데 시간이 걸린다. 그냥 더미데이터로 처리하기위해
                            # 더미데이터로 DB에 직접 저장..
                            # photo_request.content 로 의미없는 01로 구성된 데이터로 만든뒤
                            # 그 데이터를  ContentFile()로 묶어서 파일로 만들어 저장한다.

                    login(request, user)
                    messages.success(request, f"환영합니다. {user.username}님")
                    return redirect(reverse("core:home"))
                else:
                    raise KakaoException("카카오 프로파일에 ID 가 없습니다. ")
        else:
            raise KakaoException("카카오에서 code를 받아올수 없습니다. ")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = user_models.User
    context_object_name = "user_obj"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["hello"] = "Hello!!!!!!!!!!!"
    #     return context


class UpdateProfileView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = user_models.User
    template_name = "users/update_profile.html"
    fields = (
        "username",
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        self.old_username = self.request.user.username  # 유저이름이 바뀌는지 확인위해
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        user = self.object
        user.email = username
        user.save()

        if not user.username == self.old_username:  # 유저이름이 바뀌었다면 이메일을 보낸다.
            user.email_verified = False
            user.verify_email()  # 모델안의 이메일 보내는 함수 호출

        return super().form_valid(form)


class UpdatePasswordView(
    user_mixins.LoggedInOnlyView,
    user_mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update_password.html"

    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


# ############################# 참고 보관용 코드 ##################################################


class UserProfileView__(DetailView):
    """
    클래스 뷰 에서 context_data 추가하기
    """

    model = user_models.User
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello!!!!!!!!!!!"
        return context


class LoginView_old(View):
    """
    로그인 뷰의 기본동작을 파악하기 위한코드.
    """

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


class SignUpView__ModelForm(FormView):
    """
    ModelForm 으로 만들어진 폼을 이용할때의 SingnUpView
    """

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
