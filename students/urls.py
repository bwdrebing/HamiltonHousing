from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^building/([a-zA-Z1-9/(/) ]+)$', views.building, name='building-view')
]