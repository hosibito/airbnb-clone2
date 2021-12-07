from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOnlyView(UserPassesTestMixin):  # 21.9 참조
    permission_denied_message = _("Page not found")

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


class EmailLoginOnlyView(UserPassesTestMixin):
    """
    카카오,깃헙 로그인 유저는 password 수정을 못하게 하기 위해
    """

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
