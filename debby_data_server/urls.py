from django.conf.urls import url, include
from debby_data_server import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/$', views.CustomUserModelList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.SpecificCustomUserModel.as_view()),
    url(r'^bgmodels/$', views.AllBGModelList.as_view()),
    url(r'^bgmodels/user/(?P<pk>[0-9]+)/$', views.SpecificUserBGModelList.as_view()),
    url(r'^bgmodels/bgmodel/(?P<pk>[0-9]+)/$', views.SpecificBGModel.as_view()),



]
