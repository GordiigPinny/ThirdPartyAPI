from django.conf.urls import url
from ThirdPartyApp import views


urlpatterns = [
    url(r'^places/$', views.GetPlacesView.as_view()),
    url(r'^places/(?P<place_id>\d+)/$', views.GetPlaceView.as_view()),
]
