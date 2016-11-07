from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^$', views.home, name='students-home'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^building/([a-zA-Z1-9/(/) ]+)$', views.building, name='building-view'),
    url(r'^rooms/all$', views.allRooms, name='all-rooms')
]