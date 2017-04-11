# This Python file uses the following encoding: utf-8
from django.db import models
from debby_data_server.models import CustomUserModel,BGModel
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
        #Be able to  execute this method indicates user must exist with the line_id and line_token
        user = CustomUserModel.objects.get(line_id = line_id,line_token = line_token)
        #time of bgmodel is automatically build by current time
        BGModel.objects.create(user = user,**self.validated_data)

    def update(self, id, time, glucose_val):

        bgmodel = BGModel.objects.get(id = id)
        bgmodel.time = time
        bgmodel.glucose_val = glucose_val
        bgmodel.save()

'''
class FoodModelSerializer(serializers.Serializer):
    user = CustomUserModelSerializer()
    calories = models.IntegerField(required = False)
    gi_value = models.IntegerField(required = False)
    food_name = models.CharField(required = False)
    food_image_upload = models.ImageField(upload_to='FoodRecord') #??
    note = models.CharField(required = False)
    time = models.DateTimeField(required = False)

    def create(self):
        #print self.validated_data
        line_id = self.validated_data['user']['line_id']
        line_token = self.validated_data['user']['line_token']

        user = CustomUserModel.objects.get_or_create(line_id = line_id,line_token = line_token)[0]
        image_content = self.validated_data['image_content']
        foodmodel = FoodModel(user = user)

        calories = self.validated_data.get('calories',"")
        if calories!= None:
            foodmodel.calories = calories
        gi_value = self.validated_data.get('gi_value',None)
        if gi_value!= None:
            foodmodel.gi_value = gi_value
        food_name = self.validated_data.get('food_name',None)
        if food_name!= None:
            foodmodel.food_name = food_name
        note = self.validated_data.get('note',None)
        if note!= None:
            foodmodel.note = note
        foodmodel.save()

#    def update(self):
'''
