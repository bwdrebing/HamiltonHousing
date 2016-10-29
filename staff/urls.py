from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^LotteryNumber$', views.lotteryNumberInput),
    url(r'^RoomSelect$', views.RoomSelect),
    url(r'^RoomSelect/StudentInfo$', views.StudentInfo),
    url(r'^RoomSelect/ConfirmSelection$', views.ConfirmSelection),
    url(r'^home$', views.home),
    url(r'^ReviewRoom$', views.ReviewRoom),
    url(r'^ReviewRoom/ReviewStudentInfo$', views.ReviewStudentInfo),
    url(r'^ReviewRoom/ConfirmSelection$', views.ConfirmSelection),
    url(r'^editOptions', views.editOptions),
    url(r'^$', views.home),
]
