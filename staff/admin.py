from django.contrib import admin
from .models import LotteryNumber
from .models import Building
from .models import Room

admin.site.register(LotteryNumber)
admin.site.register(Building)
admin.site.register(Room)
