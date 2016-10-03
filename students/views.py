from django.shortcuts import render
from .models import Building
from .models import Room

# Home page view
def home(request):
    buildings = list(Building.objects.all())
    return render(request, 'students/home.html', {'buildings': buildings})

def building(request, building_name):
    bldg = Building.objects.get(name=building_name)
    building_list = Building.objects.order_by('name')
    #all the rooms that are in this building and that are available -- sort?
    rooms = list(Room.objects.all()
                             .filter(building=bldg)
                             .exclude(available=False)
                             .order_by('number'))
    
    # get floor numbers and create dictionary of rooms organized by floor
    # ex. {0: [001, 002, 003], 1: [101, 102, 103]}
    floors = {}
    last_floor_seen = rooms[0].number[0] # last floor number seen
    for room in rooms:
        if room.number[0] != last_floor_seen:
            last_floor_seen = room.number[0]
            floors[room.number[0]] = [room]

        else:
            floors[room.number[0]].append(room) # floor already seen, append to list
            
            
    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg, 
                   'building': bldg, 
                   'allrooms': rooms, 
                   'floors': floors,
                   'buildings': building_list})