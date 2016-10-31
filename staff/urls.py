from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lotterynumber$', views.lotteryNumberInput, name='loto-num'),
    url(r'select/suite$', views.suiteSelect, name='suite-select'),
    url(r'select/suite/studentinfo$', views.suiteStudentInfo, name='suite-select-student-info'),
    url(r'select/suite/confirm$', views.suiteConfirm, name='suite-select-confirm'),
    url(r'^select/room$', views.RoomSelect, name='room-select'),
    url(r'^select/room/studentinfo$', views.StudentInfo, name='room-select-student-info'),
    url(r'^select/room/confirmselection$', views.ConfirmSelection, name='room-select-confirm'),
    url(r'^home$', views.home, name='home'),
    url(r'^edit/transaction$', views.ReviewRoom, name='review-room'),
    url(r'^edit/transaction/studentinfo$', views.ReviewStudentInfo, name='review-room-student-info'),
    url(r'^edit/transaction/confirm$', views.ConfirmSelection, name='review-room-confirm'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^edit/building$', views.editBuilding, name = 'edit-building'),
    url(r'^edit/room$', views.editRoom, name = 'edit-room'),
    url(r'^$', views.home, name='home'),
]