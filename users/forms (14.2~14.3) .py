from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 각항목이름 앞 clean_ 으로 접근
    # 정리된 데이터 결과값에 접근하는것임
    def clean_email(self):
        # print(self.cleaned_data)  # {'email': 'test@test.com'}
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(username=email)  # 니콜라스는 유저이름을 이메일로 하는걸 선호함
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        # print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    # 이메일과 페스워드 두군데의 처리를 했으나..
    # 깔끔하지 않고 반복된다.
    # 서로 관련있는 것은 하나로 묶을수 있다.
