from debby_data_server.models import CustomUserModel,BGModel
from debby_data_server.serializers import CustomUserModelSerializer,BGModelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomUserModelList(APIView):
    """
    List all Users, or create a new User.
    """
    def get(self, request, format=None):
        customUserModels = CustomUserModel.objects.all()
        serializer = CustomUserModelSerializer(customUserModels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomUserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificCustomUserModel(APIView):
    """
    Retrieve, update or delete a CustomUserModel instance.
    """
    def get_object(self, pk):
        try:
            return CustomUserModel.objects.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customuser = self.get_object(pk)
        serializer = CustomUserModelSerializer(customuser)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customuser = self.get_object(pk)
        serializer = CustomUserModelSerializer(customuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customuser = self.get_object(pk)
        customuser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllBGModelList(APIView):
    """
    List all bgmodels, or create a new bgmodel.
    """
    def get(self, request, format=None):
        bgmodels = BGModel.objects.all()
        serializer = BGModelSerializer(bgmodels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = BGModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificUserBGModelList(APIView):
    """
    List all BModels of certain user by user__id
    """
    def get(self, request,pk, format=None):
        bgmodels = BGModel.objects.all().filter(user__line_id = pk)
        serializer = BGModelSerializer(bgmodels, many=True)
        return Response(serializer.data)

class SpecificBGModel(APIView):
    """
    Retrieve, update or delete a BGModel instance by its pk.
    """
    def get_object(self, pk):
        try:
            return BGModel.objects.get(pk=pk)
        except BGModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bgmodel = self.get_object(pk)
        serializer = BGModelSerializer(bgmodel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        bgmodel = self.get_object(pk)
        serializer = BGModelSerializer(bgmodel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bgmodel = self.get_object(pk)
        bgmodel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
