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
    building_list = Building.objects.exclude(closed=True).order_by('name')
    
    # all the rooms that are in this building and that are available
    rooms = list(Room.objects.all()
                             .filter(building=bldg)
                             .exclude(available=False)
                             .order_by('number'))
    
    # all the floor images associated with this building 
    floor_images = list(bldg.floor_plans.all().order_by('floor'))
    
    # set of floors
    floors = []
    for floorplan in floor_images:
        if floorplan.floor not in floors:
            floors.append(floorplan.floor)
    
    # get the first floor plan to display first
    if (floor_images):
        first_floorplan = floor_images[0]
    else:
        first_floorplan = None
    
    # get next lottery number for header
    number = list(LotteryNumber.objects.all())[-1]

    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg,
                   'rooms': rooms, 
                   'buildings': building_list,
                   'floors': floors,
                   'floor_images': floor_images,
                   'first_floorplan': first_floorplan,
                   'LotteryNumber': number})