# This Python file uses the following encoding: utf-8
from django.db import models
from debby_data_server.models import CustomUserModel,BGModel
from rest_framework import serializers
import datetime

class CustomUserModelSerializer(serializers.Serializer):
    line_id = serializers.CharField(max_length=33)
    line_token = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return CustomUserModel.objects.create(**validated_data)


class BGModelSerializer(serializers.Serializer):
    user = CustomUserModelSerializer()
    time = serializers.DateTimeField(required = False)
    glucose_val = serializers.IntegerField()
    type = serializers.CharField(max_length=10)

    def save(self):
        #print self.validated_data
        line_id = self.validated_data['user']['line_id']
        line_token = self.validated_data['user']['line_token']

        user = CustomUserModel.objects.get_or_create(line_id = line_id,line_token = line_token)[0]
        glucose_val = self.validated_data['glucose_val']
        type = self.validated_data['type']
        bgmodel = BGModel(user = user,glucose_val = glucose_val , type = type)
        bgmodel.save()
