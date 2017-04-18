# This Python file uses the following encoding: utf-8
from django.db import models
#from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import BaseUserManager
#from linebot.models import TextSendMessage
#from linebot.models import TemplateSendMessage
import datetime


# Custom user model for line.
# example from https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/


class CustomUserModel(models.Model): #todo:
    username_validator = None
    username = None

    line_id = models.CharField(max_length=33, unique=True)
    line_token = models.CharField(max_length=100, blank=True)

    #objects = CustomUserManager()

    USERNAME_FIELD = 'line_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.line_id


class UserSettingModel(models.Model):
    user = models.ForeignKey(CustomUserModel)
    unit = models.CharField(max_length=10,
                            choices=(
                                ('mg/dL', 'mg/dL'),
                                ('mmol/L', 'mmol/L'),
                            ),
                            default='mg/dL'
                            )

    breakfast_reminder = models.TimeField(default=datetime.time(9,00))
    breakfast_reminder_status = models.BooleanField(default=True)
    lunch_reminder = models.TimeField(default=datetime.time(12,30))
    lunch_reminder_status = models.BooleanField(default=True)
    dinner_reminder = models.TimeField(default=datetime.time(7,30))
    dinner_reminder_status = models.BooleanField(default=True)

    late_reminder = models.TimeField()
    height = models.FloatField()
    weight = models.FloatField()



class UserLogModel(models.Model):
    user = models.ForeignKey(CustomUserModel)
    request_text = models.CharField(max_length=50,
                                    verbose_name=('Request from user.'))
    response = models.CharField(max_length=50,
                                verbose_name=('Response from debby.'))
    time = models.DateTimeField(auto_now_add=True)
    #objects = UserLogManger()


class BGModel(models.Model):
    user = models.ForeignKey(CustomUserModel)
    time = models.DateTimeField(auto_now_add=True)
    glucose_val = models.IntegerField(blank=False)
    type = models.CharField(max_length=10,
                            choices=(
                                ('before', '餐前'),
                                ('after', '飯後'),
                            ),
                            default='after'
                            )

    def __str__(self):
        return self.user.line_id

class FoodModel(models.Model):
    user = models.ForeignKey(CustomUserModel)
    calories = models.IntegerField(null=True, blank=True)
    gi_value = models.IntegerField(null=True, blank=True)
    food_name = models.CharField(max_length=50)
    food_image_upload = models.ImageField(upload_to='FoodRecord')
    note = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
