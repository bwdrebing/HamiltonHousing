from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^LotteryNumber$', views.lotteryNumberInput),
    url(r'^RoomSelect$', views.RoomSelect),
    url(r'^home$', views.home),
    url(r'^$', views.home),
]
