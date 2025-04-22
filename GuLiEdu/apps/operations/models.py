from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import CourseInfo


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="手机")
    course = models.CharField(max_length=20, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "咨询信息"
        verbose_name_plural = verbose_name


class UserLove(models.Model):
    love_man = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="收藏用户")
    love_id = models.IntegerField(verbose_name="收藏id")
    love_type = models.IntegerField(choices=((1, 'org'), (2, 'course'), (3, 'teacher')), verbose_name="收藏类别")
    love_status = models.BooleanField(default=False, verbose_name="收藏状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.love_man.username

    class Meta:
        verbose_name = "收藏信息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    study_man = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="学习用户")
    study_course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, verbose_name="学习的课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.study_man.username

    class Meta:
        unique_together = ('study_man', 'study_course')
        verbose_name = "用户课程学习信息"
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    commnet_man = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="评论用户")
    commnet_course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, verbose_name="评论课程")
    comment_content = models.CharField(max_length=300, verbose_name="用户评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.commnet_man.username

    class Meta:
        verbose_name = "用户评论信息"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    message_man = models.IntegerField(default=0, verbose_name="消息用户")
    message_content = models.CharField(max_length=300, verbose_name="消息内容")
    message_status = models.BooleanField(default=False, verbose_name="消息状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.message_content

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name
