# This Python file uses the following encoding: utf-8
from django.db import models
from debby_data_server.models import CustomUserModel,BGModel,FoodModel
from rest_framework import serializers
import datetime

class CustomUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ('line_id','line_token')

    def create(self):
        return CustomUserModel.objects.create(**self.validated_data)


class BGModelSerializer(serializers.ModelSerializer):
    #user = CustomUserModelSerializer()
    class Meta:
        model = BGModel
        #fields = ('user','glucose_val','type','time')
        fields = ('id','glucose_val','type','time')

    def create(self, line_id, line_token):
        #call this method indicates indicates user must exist with the line_id and line_token
        user = CustomUserModel.objects.get(line_id = line_id,line_token = line_token)
        #time of bgmodel is automatically build by current time
        BGModel.objects.create(user = user,**self.validated_data)

    def update(self, id, time, glucose_val):

        bgmodel = BGModel.objects.get(id = id)
        bgmodel.time = time
        bgmodel.glucose_val = glucose_val
        bgmodel.save()


class FoodModelSerializer(serializers.ModelSerializer):
    #user = CustomUserModelSerializer()

    class Meta:
        model = FoodModel
        fields = ('id','calories','gi_value','food_name','food_image_upload','note','time')

    def create(self, line_id, line_token):
        #call this method indicates indicates user must exist with the line_id and line_token
        user = CustomUserModel.objects.get(line_id = line_id,line_token = line_token)
        #time of FoodModel is automatically build by current time
        foodmodel = FoodModel.objects.create(user = user)

        image_content = self.validated_data.get('image_content',None)
        if not image_content:
            io = BytesIO(image_content)
            file = '{0}_food_image.jpg'.format(user.line_id)
            foodmodel.food_image_upload.save(file,File(io))

        note = self.validated_data.get('note',None)
        if not note:
            foodmodel.note = note
            foodmodel.save()
