from __future__ import unicode_literals

from django.db import models

# Create your models here.
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
    gender_blocked = models.BooleanField(default=False)
    
    # ManyToManyField allows for a list-like collection of associated models (i think)
    floor_plans = models.ManyToManyField(
        'FloorPlan', 
        blank=True
    )

    notes = models.TextField(blank=True, default='')
    
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
    
    
class Room(models.Model):
    # Building
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
    )
    
    # Room Number
    number = models.CharField(max_length = 5)
    
    # Choices for Room Type
    SINGLE = 'S'
    DOUBLE = 'D'
    TRIPLE = 'T'
    QUAD = 'Q'
    BLOCK = 'B'
    OTHER = 'O'
    ROOM_TYPE_CHOICES = (
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (TRIPLE, 'Triple'),
        (QUAD, 'Quad'),
        (BLOCK, 'Block'),
        (OTHER, 'Other'),
    )
    
    # Room Type Field
    room_type = models.CharField(
        max_length=1,
        choices=ROOM_TYPE_CHOICES,
        default=OTHER,
    )
        
    # For taking room - student year/number/gender
    FEMALE = 'F'
    MALE = 'M'
    EITHER = 'E'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (EITHER, 'Either'),
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=EITHER,
    )
    
    # Room Pulled by this Room
    #pull = models.ForeignKey(
    #    'self',
    #    on_delete=models.CASCADE,
    #    blank=True,
    #    null=True,
    #)
    
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
    apartment_number = models.CharField(
        max_length=5,
        blank = True,
        default = '',
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
    Puller_Year = models.PositiveSmallIntegerField()

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
