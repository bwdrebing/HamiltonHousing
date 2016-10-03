from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^building/([a-zA-Z ]+)', views.building, name='building-view'),
]
