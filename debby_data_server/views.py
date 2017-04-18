from debby_data_server.models import CustomUserModel,BGModel,FoodModel
from debby_data_server.serializers import CustomUserModelSerializer,BGModelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CustomUserModelView(APIView):
    #for debug use: get all users
    def get(self, request, format=None):
        customUserModels = CustomUserModel.objects.all()
        serializer = CustomUserModelSerializer(customUserModels, many=True)
        return Response(serializer.data)

    '''
    post: create a new user, request must have line_id and line_token
    request example:
    { "line_id": "00003",
      "line_token": "00003token"}
    '''
    def post(self, request, format=None):
        serializer = CustomUserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomUserBGModelView(APIView):


    '''
    post: get all bgmodels of a user, or get first num_of_latest bgmodels(ordered by time) of a user
    request body must have line_id and line_token, num_of_latest is optional
    request example:
    { "line_id": "00003",
      "line_token": "00003token",
      "num_of_latest": 5
     }
    '''
    def post(self, request, format=None):
        #get line_id and line_token from request body
        line_id = request.data['line_id']
        line_token = request.data['line_token']
        num_of_latest = request.data.get('num_of_latest',None) #if num_of_latest == 2, this API get 2 latest bgmodels
        page_num = request.data.get('page_num',1)
        page_size = request.data.get('page_size',5)

        #use line_id and line_token to query user model table
        user = CustomUserModel.objects.filter(line_id = line_id, line_token = line_token)

        #user model does not exist -> bad request
        if not user:
            response = {"error":"user does not exist or wrong token"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:     #user model exist -> query bgmodel
            if not num_of_latest:
                bgmodels = BGModel.objects.filter(user__line_id = line_id, user__line_token=line_token)
            else:
                bgmodels = BGModel.objects.filter(user__line_id = line_id, user__line_token=line_token).order_by("-time")[:num_of_latest]
                retrive_num = num_of_latest if num_of_latest < len(bgmodels) else len(bgmodels)
                bgmodels = bgmodels[:retrive_num]

            paginator = Paginator(bgmodels, page_size)
            try:
                bgmodels = paginator.page(page_num)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                response = {"error":"page_num is not an integer"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                response = {"error":"page_num is out of range"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = BGModelSerializer(bgmodels, many=True)

            if paginator.num_pages == 1:
                response = {"line_id":line_id,"bgmodels": serializer.data}
            else: #>1
                if page_num ==1 :
                    response = {"next_page": (page_num+1) }
                elif page_num == paginator.num_pages: #last page
                    response = {"previous_page":(page_num-1)}
                else:
                    response = {"next_page": (page_num+1) ,"previous_page":(page_num-1)}
            response['num_pages'] = paginator.num_pages
            response['page_size'] = page_size
            response['line_id'] = line_id
            response['bgmodels'] = serializer.data
            return Response(response)


class BGModelView(APIView):

    #for debug use: get all bgModels
    def get(self, request, format=None):
        bgModels = BGModel.objects.all()
        serializer = BGModelSerializer(bgModels, many=True)
        response = {"bgmodels": serializer.data}
        return Response(response)

    '''
    post: create a bgmodel- request body has bgmodel , line_id and line_toekn
    request example:
    { "line_id": "00003",
      "line_token": "00003token",
      "bgmodel": {
        "id": 27,
        "glucose_val": 121,
        "time": "2017-04-14T05:13:20.798278Z"}
    }
    if user with the line_id and line_token does not exist, it will not create the user
    '''
    def post(self, request, format=None):
        bgmodel = request.data['bgmodel']
        serializer = BGModelSerializer(data=bgmodel)
        line_id = request.data['line_id']
        line_token = request.data['line_token']


        user = CustomUserModel.objects.filter(line_id = line_id, line_token = line_token)

        if not user:  #user model does not exist -> bad request
            response = {"error":"user does not exist or wrong token"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.create(line_id,line_token)
            response = {"line_id":line_id ,"bgmodel": serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    put: update a bgmodel - request body must have id, glucose_val, time , line_id and line_token
    request example:
    { "line_id": "00003",
      "line_token": "00003token",
      "bgmodel": {
        "id": 27,
        "glucose_val": 121,
        "time": "2017-04-14T05:13:20.798278Z"}
    }
    if you only want to update one of time and glucose_val, you still have to provide both time and glucose_val.
    '''
    def put(self, request, format=None):

        bgmodel = request.data['bgmodel']
        #to-do: find the reason why id, and time field disappear after serialization
        serializer = BGModelSerializer(data=request.data['bgmodel'])

        line_id = request.data['line_id']
        line_token = request.data['line_token']

        id = request.data['bgmodel']['id']
        time = request.data['bgmodel']['time']
        glucose_val = request.data['bgmodel']['glucose_val']

        user = CustomUserModel.objects.filter(line_id = line_id, line_token = line_token)
        if not user:  #user model does not exist -> bad request
            response = {"error":"user does not exist or wrong token"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.update(id,time,glucose_val)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    delete: delete a bgmodel - request parameter must have id of bgmodel
    request parameter: "id"
    '''
    def delete(self, request, id,format=None):

        bgmodel = BGModel.objects.filter(id=id)
        if bgmodel.exists():
            bgmodel.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response( {"error":"id does not exist"},status=status.HTTP_400_BAD_REQUEST)



class FoodModelView(APIView):

    def post(self, request, format=None):
        foodmodel = request.data['foodmodel']
        serializer = FoodModelSerializer(data=foodmodel)
        line_id = request.data['line_id']
        line_token = request.data['line_token']


        user = CustomUserModel.objects.filter(line_id = line_id, line_token = line_token)

        if not user:  #user model does not exist -> bad request
            response = {"error":"user does not exist or wrong token"}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.create(line_id,line_token)
            response = {"line_id":line_id ,"foodmodel": serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
