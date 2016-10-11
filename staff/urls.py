from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^LotteryNumber$', views.lotteryNumberInput),
    url(r'^RoomSelect$', views.RoomSelect),
    url(r'^home$', views.home),
    url(r'^upload$', views.upload),
    url(r'^import$', views.import_data),
    url(r'^$', views.home),
]
