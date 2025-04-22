"""
Author: WangXing
Time: 2025/3/13 20:02
Description:
"""
from users.models import EmailVerifyCode
from random import randint
from django.core.mail import send_mail
from GuLiEdu.settings import DEFAULT_FROM_EMAIL


def get_random_code(code_length):
    code = ""
    for _ in range(code_length):
        code_num = randint(0, 9)  # 生成 code_length 个 0-9 之间的随机整数
        code += str(code_num)
    return code


def send_email_code(email, send_type):
    # 创建邮箱验证码对象，保存数据库，以后用来对比
    code = get_random_code(5)
    a = EmailVerifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()

    # 发送邮件到邮箱
    send_title = ''
    send_boy = ''
    if send_type == 1:
        send_title = "欢迎注册星仔教育系统"
        send_boy = "请点击以下链接激活:\n http://127.0.0.1:8000/users/user_activate/" + code
        send_mail(send_title, send_boy, DEFAULT_FROM_EMAIL, [email])
    if send_type == 2:
        send_title = "星仔教育系统重置密码"
        send_boy = "请点击以下链接重置你的密码:\n http://127.0.0.1:8000/users/user_reset/" + code
        send_mail(send_title, send_boy, DEFAULT_FROM_EMAIL, [email])
    if send_type == 3:
        send_title = "星仔教育系统修改密码"
        send_boy = "您的验证码是" + code
        send_mail(send_title, send_boy, DEFAULT_FROM_EMAIL, [email])
