from django.shortcuts import render
from .models import Building
from .models import Room
from .models import LotteryNumber
from .models import PageContent
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
        
    pageContent = PageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
        
    return render(request, 'students/home.html', {'buildings': buildings,
                                                  'pageContent': pageContent,
                                                  'LotteryNumber': number})


# organize rooms by floor
def get_rooms_by_floor(rooms):
    """A function that returns a dictionary of dictionarys!
       param bldg is a Building object from the building view
       returned object looks like this: {'1': {'101': <Room object 101>
                                               '10': [<Room object 110>, <Room object 152>]}}}
    """
    
    # initialize dictionary to organize rooms by floor for filtering
    rooms_dict = collections.OrderedDict()
    show_gender = False
    show_pull = False
    show_notes = False
    room_types = []
    floors = []
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        floor = room.floor
        show_gender = (show_gender or (room.gender != 'E'))
        show_pull = (show_pull or room.pull)
        show_notes = (show_notes or room.notes)
        
        if floor not in floors:
            floors.append(floor)
        
        if room.room_type not in room_types:
            room_types.append(room.room_type)
            
        # if this room is in an apartment
        if room.apartment:
            show_gender = (show_gender or (room.apartment.gender != 'E'))
            show_notes = (show_notes or room.apartment.notes)
            
            # if the apartment is already in the dict
            if room.apartment.number in rooms_dict:
                rooms_dict[room.apartment.number].append(room)
                    
            # if this specific apt has not been initialized
            else:
                rooms_dict[room.apartment.number] = [room]
                                                                
        else:
            rooms_dict[room.number] = [room]
                
    return (rooms_dict, show_gender, show_pull, show_notes, room_types, floors)     

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
    
    rooms, show_gender, show_pull, show_notes, room_types, floors = get_rooms_by_floor(rooms)
    
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    
    return render(request, 
                  'students/building.html', 
                  {'current_building': bldg,
                   'rooms': rooms, 
                   'show_gender': show_gender,
                   'show_pull': show_pull,
                   'show_notes': show_notes,
                   'room_types': room_types,
                   'floors': floors,
                   'buildings': building_list,
                   'floor_images': floor_images,
                   'LotteryNumber': number})

# organize all rooms into a dict and collect info about them
def all_rooms_with_filters(rooms):
    """A function that returns a dictionary of dictionarys!
       param bldg is a Building object from the building view
       returned object looks like this: {'1': {'101': <Room object 101>
                                               '10': [<Room object 110>, <Room object 152>]}}}
    """
    
    # initialize dictionary to organize rooms by floor for filtering
    rooms_dict = collections.OrderedDict()
    show_gender = False
    show_pull = False
    room_types = []
    floors = []
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        floor = room.floor
        show_gender = (show_gender or (room.gender != 'E'))
        show_pull = (show_pull or room.pull)
        
        if floor not in floors:
            floors.append(floor)
        
        if room.room_type not in room_types:
            room_types.append(room.room_type)
            
        # if this room is in an apartment
        if room.apartment:
            show_gender = (show_gender or (room.apartment.gender != 'E'))
            
            # if the apartment is already in the dict
            if str(room.apartment) in rooms_dict:
                rooms_dict[str(room.apartment)].append(room)
                    
            # if this specific apt has not been initialized
            else:
                rooms_dict[str(room.apartment)] = [room]
                                                                
        else:
            rooms_dict[str(room)] = [room]
                
    return (rooms_dict, show_gender, show_pull, room_types, floors)  

def allRooms(request):
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
    rooms = list(Room.objects.exclude(available = False)
                             .exclude(available_beds = 0)
                             .order_by('number'))
    
    rooms, show_gender, show_pull, room_types, floors = all_rooms_with_filters(rooms)
    
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
        
    return render(request, 
                  'students/all.html', 
                  {'buildings': building_list,
                   'rooms': rooms,
                   'show_gender': show_gender,
                   'show_pull': show_pull,
                   'room_types': room_types,
                   'floors': floors,
                   'LotteryNumber': number})

def contact(request):
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
     # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
        
    return render(request, 
                  'students/contact.html', 
                  {'buildings': building_list,
                   'LotteryNumber': number})