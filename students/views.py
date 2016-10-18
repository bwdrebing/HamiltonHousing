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
            
    # initialize values to calculate building stats
    rooms_left = 0
    singles = 0
    doubles = 0
    triples = 0
    quads = 0
    
    # initialize dictionary to organize rooms by floor for filtering
    rooms_by_floor = { }
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        if room.room_type == 'S':
            singles += 1
        if room.room_type == 'D':
            doubles += 1
        if room.room_type == 'T':
            triples += 1
        if room.room_type == 'Q':
            quads += 1
            
        rooms_left += 1
        
        # append room to appropriate floor list
        if room.number[0] in rooms_by_floor:
            rooms_by_floor[room.number[0]].append(room)
        else:
            rooms_by_floor[room.number[0]] = [room]
            
    # floors represented here are the keys in the dictionary
    floors = [ floor for floor in rooms_by_floor.keys() ]
    floors.sort()
    num_floors = len(floors)
        
    building_stats = {
        'rooms_left': rooms_left,
        'singles': singles,
        'doubles': doubles,
        'triples': triples,
        'quads': quads
    }
    
    # get next lottery number for header
    number = list(LotteryNumber.objects.all())[-1]
    
    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg,
                   'rooms_by_floor': rooms_by_floor, 
                   'buildings': building_list,
                   'floors': floors,
                   'num_floors': num_floors,
                   'floor_images': floor_images,
                   'LotteryNumber': number,
                   'building_stats': building_stats})