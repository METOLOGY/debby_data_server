from django.conf.urls import url, include
from debby_data_server import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/users/$', views.CustomUserModelList.as_view()),
    url(r'^api/v1/users/(?P<line_id>[a-zA-Z0-9_]+)/$', views.SpecificCustomUserModel.as_view()),
    url(r'^api/v1/bgmodels/$', views.AllBGModelList.as_view()),
    url(r'^api/v1/bgmodels/user/(?P<line_id>[a-zA-Z0-9_]+)/$', views.SpecificUserBGModelList.as_view()),
    url(r'^api/v1/bgmodels/bgmodel/(?P<pk>[0-9]+)/$', views.SpecificBGModel.as_view()), #pk is id



]
