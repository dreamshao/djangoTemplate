"""
Author: WangXing
Time: 2025/3/21 19:37
Description:
"""
from django import forms
from .models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'course', 'phone']
        # 用到所有模型的字段校验
        # fields = "__all__"
        # exclude = ['add_time'] 去除add_time 验证

    def clean_phone(self):
        # 再次对具体的信息做验证 必须要clean_字段名这样的去写
        phone = self.cleaned_data['phone']
        if not phone:
            com = False
        # 移动
        elif re.match(r'^1(34[0-8]|(3[5-9]|47|5[0-2]|57[124]|5|8[2378]))\d{7}$', phone):
            com = True
        # 联通
        elif re.match(r'^1(3[0-2]|45|5|8)\d{8}$', phone):
            com = True
        # 电信
        elif re.match(r'^1(33|53|8)\d{8}$', phone):
            com = True
        else:
            com = False
        if com:
            return phone
        else:
            raise forms.ValidationError("手机号码不合法")


class UserCommentForm(forms.Form):
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=1, max_length=300)
