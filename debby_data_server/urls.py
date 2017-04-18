from django.conf.urls import url, include
from debby_data_server import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #post: create a user  #todo: get a user
    url(r'^api/v1/user/$', views.CustomUserModelView.as_view()),

    #todo: post:get a user information
    #url(r'^api/v1/user/info$'),

    #post: get bgmodels of a user
    url(r'^api/v1/user/bgmodels/$', views.CustomUserBGModelView.as_view()),

    #post: create a bgmodel (by line_id,line_token, and a bgmodel)
    #put: update a bgmodel  (by line_id,line_token, and id of bgmodel)
    url(r'^api/v1/bgmodel/$', views.BGModelView.as_view()),

    #delete: update a bgmodel  (by line_id,line_token, and id of bgmodel)
    url(r'^api/v1/bgmodel/(?P<id>[A-Za-z0-9]+)/$', views.BGModelView.as_view()),
    #post: create a food model
    #put: update a food model
    url(r'^api/v1/foodmodel/$', views.FoodModelView.as_view()),
]
