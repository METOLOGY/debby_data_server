from django.conf.urls import url, include
from debby_data_server import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #post: create a user
    url(r'^api/v1/user/$', views.CustomUserModelView.as_view()),

    #post: get bgmodels of a user
    url(r'^api/v1/user/bgmodels/$', views.CustomUserBGModelView.as_view()),

    #post: create a bgmodel by line_id,line_token, and a bgmodel
    #put: update a bgmodel
    url(r'^api/v1/bgmodel/$', views.BGModelView.as_view()),

    #post: create a food model
    #put: update a food model
    url(r'^api/v1/foodmodel/$', views.FoodModelView.as_view()),
]
