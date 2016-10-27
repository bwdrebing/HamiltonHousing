from django.shortcuts import render
from .models import Building
from .models import Room
from .models import LotteryNumber
import collections                  # for the ordered dictionary

# Home page view
def home(request):
    buildings = list(Building.objects.all().exclude(available=False).order_by('name'))
    
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    return render(request, 'students/home.html', {'buildings': buildings,
                                                  'LotteryNumber': number})


# organize rooms by floor
def get_rooms_by_floor(rooms):
    """A function that retuns a dictionary of dictionarys!
       param bldg is a Building object from the building view
       returned object looks like this: {'rooms_left': 0
                                         'apts_left': 0,
                                         'singles': 0,
                                         'doubles': 0,
                                         'triples': 0,
                                         'quads': 0,
                                         'rooms_by_floor': {'1': {'101': ""
                                                                  '10': ['101', '110', '152']}}}
    """
    
     # initialize values to calculate building stats
    rooms_left = 0
    apts_left = 0
    singles = 0
    doubles = 0
    triples = 0
    quads = 0
    
    # initialize dictionary to organize rooms by floor for filtering
    rooms_by_floor = collections.OrderedDict()
        
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
            
        floor = room.number[0]
        
        # if this room is in an apartment
        if room.apartment_number:
            rooms_left += 1
            
            # if the floor is already a key
            if floor in rooms_by_floor:
                
                # if this specific apt has been initialized as a key
                if room.apartment_number in rooms_by_floor[floor]:
                    rooms_by_floor[floor][room.apartment_number].append(room)
                    
                # if this specific apt has not been initialized
                else:
                    apts_left += 1
                    rooms_by_floor[floor][room.apartment_number] = [room]
            else:
                rooms_by_floor[floor] = collections.OrderedDict([(room.apartment_number,
                                                                  [room])])
                                                                
        else:
            rooms_left += 1
            
            # if the floor is already a key
            if floor in rooms_by_floor:
                rooms_by_floor[floor][room.number] = [room]
                
            # the floor is not a key
            else:
                rooms_by_floor[floor] = collections.OrderedDict([(room.number, [room])])
                
    return {'building_stats': {
                'rooms_left': rooms_left,
                'apts_left': apts_left,
                'singles': singles,
                'doubles': doubles,
                'triples': triples,
                'quads': quads
            },
            'rooms_by_floor': rooms_by_floor}
            

# Building page view
def building(request, building_name):
    bldg = Building.objects.get(name=building_name)
    building_list = Building.objects.exclude(available=False).order_by('name')
    
    # all the rooms that are in this building and that are available
    rooms = list(Room.objects.all()
                             .filter(building=bldg)
                             .exclude(available=False)
                             .exclude(available_beds = 0)
                             .order_by('number'))
    
    # all the floor images associated with this building 
    floor_images = list(bldg.floor_plans.all().order_by('floor'))
    
    rooms_by_floor = get_rooms_by_floor(rooms)
    rooms = rooms_by_floor['rooms_by_floor']
    building_stats = rooms_by_floor['building_stats']
               
    # floors represented here are the keys in the dictionary
    floors = [ floor for floor in rooms.keys() ]
    floors.sort()
    num_floors = len(floors)
    
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    
    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg,
                   'rooms_by_floor': rooms, 
                   'buildings': building_list,
                   'floors': floors,
                   'num_floors': num_floors,
                   'floor_images': floor_images,
                   'LotteryNumber': number,
                   'building_stats': building_stats})