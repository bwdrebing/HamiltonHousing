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
    """A function that returns a dictionary of dictionarys!
       param bldg is a Building object from the building view
       returned object looks like this: {'1': {'101': <Room object 101>
                                               '10': [<Room object 110>, <Room object 152>]}}}
    """
    
    # initialize dictionary to organize rooms by floor for filtering
    rooms_by_floor = collections.OrderedDict()
    show_gender = False
    show_pull = False
    show_notes = False
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        floor = room.floor
        show_gender = (show_gender or (room.gender != 'E'))
        show_pull = (show_pull or room.pull)
        show_notes = (show_notes or room.notes)
            
        # if this room is in an apartment
        if room.apartment_number:
            
            # if the floor is already a key
            if floor in rooms_by_floor:
                
                # if this specific apt has been initialized as a key
                if room.apartment_number in rooms_by_floor[floor]:
                    rooms_by_floor[floor][room.apartment_number].append(room)
                    
                # if this specific apt has not been initialized
                else:
                    rooms_by_floor[floor][room.apartment_number] = [room]
                    
            else:
                rooms_by_floor[floor] = collections.OrderedDict([(room.apartment_number,
                                                                [room])])
                                                                
        else:
            # if the floor is already a key
            if floor in rooms_by_floor:
                rooms_by_floor[floor][room.number] = [room]
                
            # the floor is not a key
            else:
                rooms_by_floor[floor] = collections.OrderedDict([(room.number, [room])])
                
    return (rooms_by_floor, show_gender, show_pull, show_notes)     

# Building page view
def building(request, building_name):
    bldg = Building.objects.get(name = building_name)
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
    # all the rooms that are in this building and that are available
    rooms = list(Room.objects.all()
                             .filter(building=bldg)
                             .exclude(available=False)
                             .exclude(available_beds = 0)
                             .order_by('number'))
    
    # all the floor images associated with this building 
    floor_images = list(bldg.floor_plans.all().order_by('floor'))
    
    rooms_by_floor, show_gender, show_pull, show_notes = get_rooms_by_floor(rooms)
               
    # floors represented here are the keys in the dictionary
    floors = [ floor for floor in rooms_by_floor.keys() ]
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
                   'rooms_by_floor': rooms_by_floor, 
                   'show_gender': show_gender,
                   'show_pull': show_pull,
                   'show_notes': show_notes,
                   'buildings': building_list,
                   'floors': floors,
                   'num_floors': num_floors,
                   'floor_images': floor_images,
                   'LotteryNumber': number})