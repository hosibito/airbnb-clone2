from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        # print(self.cleaned_data)  # {'email': 'lalalalal', 'password': 'argare'}
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data  # 데이터 전체를 리턴
            else:
                # raise forms.ValidationError("Password is wrong")
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error("email", forms.ValidationError("User does not exist"))


"""
    14.3~14.4 참조
"""


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):  # 순차적 처리
        password = self.cleaned_data.get("password")  # 순차적처리를 햇으므로 password 를 가져올수 있다.
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):  # 이걸.. forms에 둘지 views에 둘지는 고민해야할 문제임.
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # models.User.objects.create()  보통은 이걸 사용해야 하나. 유저는 password를 암호화해야한다.
        user = models.User.objects.create_user(email, email, password)
        # 장고 usermodel에서 제공.. username,email,password 순이나 유저네임을 이메일로 이용할것이므로...
        user.first_name = first_name
        user.last_name = last_name
        user.save()
