from django.shortcuts import render
from .models import Building
from .models import Room
from .models import LotteryNumber

# Home page view
def home(request):
    buildings = list(Building.objects.all().order_by('name'))
    
    # get next lottery number for header
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'students/home.html', {'buildings': buildings,
                                                  'LotteryNumber': number})

# Building page view
def building(request, building_name):
    bldg = Building.objects.get(name=building_name)
    building_list = Building.objects.order_by('name')
    
    # all the rooms that are in this building and that are available
    rooms = list(Room.objects.all()
                             .filter(building=bldg)
                             .exclude(available=False)
                             .order_by('number'))
    
    # get next lottery number for header
    number = list(LotteryNumber.objects.all())[-1]
            
    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg, 
                   'building': bldg, 
                   'rooms': rooms, 
                   'buildings': building_list,
                   'LotteryNumber': number})