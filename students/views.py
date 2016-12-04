from django.shortcuts import render
from .models import Building, Room, LotteryNumber, StudentPageContent, FAQ
import collections                  # for the ordered dictionary

from .forms import ContactForm

# for contact view (emailing)
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template

# Home page view
def home(request):
    buildings = list(Building.objects.all().exclude(available=False).order_by('name'))
    
    # get next lottery number for header
    try:
        number = LotteryNumber.objects.latest()
    except:
        number = ""
        
    pageContent = StudentPageContent.objects.filter(active=True)
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
    rooms_list = []
    apts_dict = collections.OrderedDict()
    room_types = []
    floors = []
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        floor = room.floor
        
        if floor not in floors:
            floors.append(floor)
        
        if room.room_type not in room_types:
            room_types.append(room.room_type)
            
        # if this room is in an apartment
        if room.apartment:
            
            # if the apartment is already in the dict
            if room.apartment.number in apts_dict:
                apts_dict[room.apartment.number].append(room)
                    
            # if this specific apt has not been initialized
            else:
                apts_dict[room.apartment.number] = [room]
                                                                
        else:
            rooms_list.append(room)
                
    return (rooms_list, apts_dict, room_types, floors)     

# Building page view
def building(request, building_name):
    building_list = (Building.objects.exclude(available=False)
                                     .order_by('name'))
    bldg = Building.objects.get(name = building_name)
    
    # get next lottery number for header
    try:
        number = LotteryNumber.objects.latest()
    except:
        number = ""

    pageContent = StudentPageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
    
    # all the rooms that are in this building and that are available
    if (bldg.available):
        rooms = list(Room.objects.all()
                                 .filter(building=bldg)
                                 .exclude(available=False)
                                 .exclude(available_beds = 0)
                                 .order_by('number'))
    
        # all the floor images associated with this building 
        floor_images = list(bldg.floor_plans.all().order_by('floor'))
        floor_image_groups = []
        for i in range(len(floor_images) // 3):
            floor_image_groups.append(floor_images[i:i+2])
            
        print(floor_image_groups)

        rooms, apts, room_types, floors = get_rooms_by_floor(rooms)

        return render(request, 
                      'students/building.html', 
                      {'current_building': bldg,
                       'rooms': rooms, 
                       'apts': apts,
                       'room_types': room_types,
                       'floors': floors,
                       'buildings': building_list,
                       'floor_images': floor_images,
                       'floor_image_groups': floor_image_groups,
                       'LotteryNumber': number,
                       'pageContent': pageContent})
    else:
        return render(request,
                      'students/unavailable_building.html',
                      {'current_building': bldg,
                       'buildings': building_list,
                       'LotteryNumber': number,
                       'pageContent': pageContent})

# organize all rooms into a dict and collect info about them
def get_room_types(rooms):
    # initialize dictionary to organize rooms by floor for filtering
    room_types = []
        
    # loop through rooms to calculate building stats & organize rooms by floor
    for room in rooms:
        if room.room_type not in room_types:
            room_types.append(room.room_type)
            
    return room_types  

def allRooms(request):
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
    rooms = list(Room.objects.exclude(available = False)
                             .exclude(available_beds = 0)
                             .order_by('building', 'number'))
    
    # room_types = get_room_types(rooms)
    room_types=['S', 'D', 'Q', 'T']
    
    # get next lottery number for header
    try:
    	number = LotteryNumber.objects.latest()
    except:    
        number = ""
    
    pageContent = StudentPageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
        
    return render(request, 
                  'students/all.html', 
                  {'buildings': building_list,
                   'current_page': 'all-rooms',
                   'rooms': rooms,
                   'room_types': room_types,
                   'LotteryNumber': number,
                   'pageContent': pageContent})

def faq(request):
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
    # get next lottery number for header
    try: 
        number = LotteryNumber.objects.latest()
    except:
        number = ""
    
    pageContent = StudentPageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
        
    faqs = FAQ.objects.order_by('number')
        
    return render(request, 
                  'students/faq.html', 
                  {'buildings': building_list,
                   'LotteryNumber': number,
                   'pageContent': pageContent,
                   'faqs': faqs})


def contact(request):
    building_list = (Building.objects.exclude(available = False)
                                     .order_by('name'))
    
    # get next lottery number for header
    try: 
        number = LotteryNumber.objects.latest()
    except:
        number = ""
        
    pageContent = StudentPageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
    return render(request, 
          'students/contact.html', 
          {'buildings': building_list,
           'LotteryNumber': number,
           'pageContent': pageContent})
