from __future__ import unicode_literals

from django.db import models
from datetime import datetime

class LotteryNumber(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.number)
    
class Building(models.Model):
    name = models.CharField(max_length = 100)
    available = models.BooleanField(blank=True, default=True)
    total_rooms = models.PositiveSmallIntegerField(default=0)
    total_singles = models.PositiveSmallIntegerField(default=0)
    total_doubles = models.PositiveSmallIntegerField(default=0)
    total_triples = models.PositiveSmallIntegerField(default=0)
    total_quads = models.PositiveSmallIntegerField(default=0)
    total_fivepulls = models.PositiveSmallIntegerField(default=0)
    total_sixpulls = models.PositiveSmallIntegerField(default=0)
    total_beds = models.PositiveSmallIntegerField(default=0)
    
    #Gender Blocking Choices, can be closed to men, closed to women, or none
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'None'),
    )
    
    closed_to = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N', # None
    )
    
    # ManyToManyField allows for a list-like collection of associated models (i think)
    floor_plans = models.ManyToManyField(
        'FloorPlan', 
        blank=True
    )

    notes = models.TextField(blank=True, default='') 
    
    def get_available_rooms(self):
        return (Room.objects.filter(building = self)
                           .filter(available = True)
                           .exclude(available_beds = 0)
                           .count())
    
    def get_available_singles(self):
        return (Room.objects.filter(building = self)
                            .filter(available = True)
                            .exclude(available_beds = 0)
                            .filter(room_type = 'S')
                            .count())
            
    def get_available_doubles(self):
        return (Room.objects.filter(building = self)
                            .filter(available = True)
                            .exclude(available_beds = 0)
                            .filter(room_type = 'D')
                            .count())
                    
    def get_available_triples(self):
        return (Room.objects.filter(building = self)
                            .filter(available = True)
                            .exclude(available_beds = 0)
                            .filter(room_type = 'T')
                            .count())
        
    def get_available_quads(self):
        return (Room.objects.filter(building = self)
                            .filter(available = True)
                            .exclude(available_beds = 0)
                            .filter(room_type = 'Q')
                            .count())
        
    available_rooms = property(get_available_rooms)    
    available_singles = property(get_available_singles)   
    available_doubles = property(get_available_doubles)   
    available_triples = property(get_available_triples)   
    available_quads = property(get_available_quads) 
    
    def __str__(self):
        return self.name

    
# returns a filepath for an image in the format MEDIA_ROOT/floorplan/building/floor/image
def building_directory_path(instance, filename):
    return 'floorplan/' + instance.related_building.name + '/' + str(instance.floor) + '/' + filename
    
class FloorPlan(models.Model):
    # the building this floor plan is from
    related_building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        null=True,
        verbose_name = 'building' # the name that the user inputting data will see
    )
   
    floor = models.PositiveSmallIntegerField()

    # user input display name for floor plan (to be display on website)
    display_name = models.CharField(
        max_length = 25, 
        default="",
        help_text="This will be the title of the image displayed to students. Ex. Floor 1 (West)"
    )

    image = models.ImageField(
        upload_to=building_directory_path
    )
    
    def __str__(self):
        return str(self.related_building.name) + " " + str(self.display_name)
    
    
class ApartmentManager(models.Manager):
    def create_apartment(self, building, number, gender="E", notes=""):
        apt = self.create(building = building, number = number, gender = gender, notes = notes)
        return apt

class Apartment(models.Model):
    objects = ApartmentManager()
    
    # Building
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
    )
    
    # Apartment Number/Name 
    number = models.CharField(max_length = 10)
    
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('E', 'Either'),
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='E', # Either
    )
    
    notes = models.TextField(blank=True, default='')
    
    def _get_available_beds(self):
        available_beds = 0
        rooms = (Room.objects.filter(apartment = self)
                             .filter(available = True)
                             .exclude(available_beds = 0))
        for room in rooms:
            available_beds += room.available_beds
            
        return available_beds
    
    def _get_room_types(self):
        room_types = ""
        rooms = (Room.objects.filter(apartment = self)
                             .filter(available = True)
                             .exclude(available_beds = 0))
        for room in rooms:
            room_types += " type" + room.room_type
            
        return room_types
    
    def _get_floors(self):
        floors = ""
        rooms = (Room.objects.filter(apartment = self)
                             .filter(available = True)
                             .exclude(available_beds = 0))
        for room in rooms:
            floors += " floor" + room.floor
            
        return floors
    
    available_beds = property(_get_available_beds)
    room_types = property(_get_room_types)
    floors = property(_get_floors)
    
    def __str__(self):
        return str(self.building.name) + " " + str(self.number)
    
    
class Room(models.Model):
    # Building
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
    )
    
    # Room Number
    number = models.CharField(max_length = 5)
    
    # Choices for Room Type
    ROOM_TYPE_CHOICES = (
        ('S', 'Single'),
        ('D', 'Double'),
        ('T', 'Triple'),
        ('Q', 'Quad'),
        ('B', 'Block'),
        ('O', 'Other'),
    )
    
    # Room Type Field
    room_type = models.CharField(
        max_length=1,
        choices=ROOM_TYPE_CHOICES,
        default='O', # Other
    )
        
    # For taking room - student year/number/gender
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('E', 'Either'),
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='E', # Either
    )
    
    pull = models.CharField(
        max_length = 5,
        default = '',
        blank=True
    )
    
    # Total Number of Beds in Room
    total_beds = models.PositiveSmallIntegerField(default = 0)
    
    # Currently Available Number of Beds
    available_beds = models.PositiveSmallIntegerField(default = 0)
    
    # Room Availabilty Status
    available = models.BooleanField(default = False)
    
    # True if this room is part of an apartment
    apartment = models.ForeignKey(
        'Apartment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="If this room is part of an apartment, this is the apartment's number/name"
    )
    
    # Notes - SPECIFICS1 
    notes = models.TextField(
        default = '',
        blank=True
    )
    
    # Notes2 - SPECIFICS2
    notes2 = models.TextField(
        default = '',
        blank=True
    )
    
    def _calculate_floor(self):
        return self.number[0]
    
    floor = property(_calculate_floor)
    
    def __str__(self):
        return (str(self.building) + " " + str(self.number))


class Transaction(models.Model):
    #Stores the lottery number, room, and year of each puller and pullee
    #So someone who did not pull anyone, the pullee information will be None
    Puller_Number = models.PositiveSmallIntegerField()
    Puller_Room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name = 'Puller_Room',
    )
    Puller_Year = models.PositiveSmallIntegerField(null=True, blank=True)

    FEMALE = 'F'
    MALE = 'M'
    EITHER = 'E'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (EITHER, 'Either'),
    )

    Puller_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                                     default=EITHER)
    
    Pullee_Number = models.PositiveSmallIntegerField(blank=True, null=True)
    Pullee_Room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name = "Pullee_Room",
        blank=True,
        null=True,
    )

    Pullee_Year = models.PositiveSmallIntegerField(blank = True, null=True)

    Pullee_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                                     default=EITHER)

    def __str__(self):

        toReturn = '#' + str(self.Puller_Number)
        if(self.Pullee_Number == None):
            toReturn += " took a room"
        else:
            toReturn += ' pulled #' + str(self.Pullee_Number)

        return toReturn
    
class BlockTransaction(models.Model):
    """Store the block number, suite, and the genders of all students in the block"""
    block_number = models.PositiveSmallIntegerField()
    suite = models.ForeignKey(
        'Room',
        on_delete = models.CASCADE,
    )
    
    residents = models.ManyToManyField(
        'Resident', 
        blank=True
    )

    def __str__(self):
        return str(self.suite) + ' taken by block ' + str(self.block_number)

class Resident(models.Model):
    class_year = models.PositiveSmallIntegerField(null = True, blank = True)
    lottery_number = models.PositiveSmallIntegerField(null = True, blank = True)
    
    FEMALE = 'F'
    MALE = 'M'
    EITHER = 'E'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (EITHER, 'Either'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=EITHER)
    
    def __str__(self):
        string = ""
        if (self.class_year and self.lottery_number and self.gender):
            string = "student(" + str(self.class_year) + ", " + \
                     str(self.lottery_number) + ", " + str(self.gender) + ")"
        elif (self.gender):
            string = "student(" + str(self.gender) + ")"
            
        return string
    
class PageContent(models.Model):
    name = models.CharField(
        max_length=50,
        default="General Lottery page content"
    )
    
    header_text = models.CharField(
        max_length=50,
        default="Let the search begin",
        help_text="This text will be displayed on the students home page as a page title",
        verbose_name="Home page main text"
    )
    
    header_subtext = models.TextField(
        default="Select a building from the left sidebar to view room availability by building",
        help_text="This text will be displayed on the home page below the title in a smaller font",
        verbose_name="Home page lead text"
    )
        
    header_block_text = models.TextField(
        default="", 
        blank=True,
        help_text="This text will be displayed as a paragraph below the page title and subtitle",
        verbose_name="Home page block text"
    )
  
    lottery_name = models.CharField(
        max_length=25,
        default="General Lottery",
        help_text="This is the name of the current lotter; it will display on the home page"
    )
    
    lottery_text = models.TextField(
        default='The General Lottery provides students an opportunity to select all other housing options not chosen in the Blocking, Co-Op and Substance-Free lotteries or otherwise pre-assigned. You do not need to sign up for the General Lottery. For more information about the lottery visit the <a href="https://www.hamilton.edu/offices/residentiallife/lottery/general-lottery">Office of Residential Life website</a>.',
        help_text="This is a description of the logistics of the this lottery"
    )
    
    contact = models.TextField(
        default='For questions or comments about the use of this website, please fill out our <a href="{% url \'contact\' %}">contact form</a>.\n\nQuestions pertaining to the lottery and the lottery process should be directed to Ashley Place, assistant director of Residential Life, at <a href="mailto:aplace@hamilton.edu">aplace@hamilton.edu</a>.',
        help_text="This is a block of text explaining who to contact with any immediate questions."
    )
    
    active = models.BooleanField(default=True)
    
    updated = models.DateTimeField(auto_now=True, blank=True)
    
    class Meta:
        get_latest_by = "updated"
    
    def __str__(self):
        return self.name