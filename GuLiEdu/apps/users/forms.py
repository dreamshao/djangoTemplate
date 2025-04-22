"""
Author: WangXing
Time: 2025/3/13 17:52
Description:
"""

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile, EmailVerifyCode


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=15,
                               error_messages={"required": "password must be input",
                                               "min_length": "password must > 3 length",
                                               "max_length": "password must be < 15 length"})
    captcha = CaptchaField()  # ✅ 添加验证码


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=15,
                               error_messages={"required": "password must be input",
                                               "min_length": "password must > 3 length",
                                               "max_length": "password must be < 15 length"})


class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()  # ✅ 添加验证码


class UserResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=3, max_length=15,
                               error_messages={"required": "password must be input",
                                               "min_length": "password must > 3 length",
                                               "max_length": "password must be < 15 length"})
    password1 = forms.CharField(required=True, min_length=3, max_length=15,
                                error_messages={"required": "password must be input",
                                                "min_length": "password must > 3 length",
                                                "max_length": "password must be < 15 length"})
    # captcha = CaptchaField()  # ✅ 添加验证码


class UserChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'address', 'phone', 'birthday']


class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


class UserResetEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email', 'code']
