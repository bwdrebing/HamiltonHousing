from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LotteryNumber(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.number)


class Building(models.Model):
    name = models.CharField(max_length = 100)
    total_rooms = models.PositiveSmallIntegerField(blank= True)
    total_floors = models.PositiveSmallIntegerField(blank= True, default = 0)
    total_singles = models.PositiveSmallIntegerField(blank= True)
    total_doubles = models.PositiveSmallIntegerField(blank= True)
    total_triples = models.PositiveSmallIntegerField(blank= True)
    total_quads = models.PositiveSmallIntegerField(blank= True)
    total_beds = models.PositiveSmallIntegerField(blank= True)
    location = models.CharField(max_length = 100, blank = True)
    gender_blocked = models.BooleanField(default = False)
    closed = models.BooleanField(blank = True, default = False)
    notes = models.TextField(blank=True, default = '')
    
    # ManyToManyField allows for a list-like collection of associated models (i think)
    floor_plans = models.ManyToManyField(
        'FloorPlan', 
        blank=True
    )
    
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
    OTHER = 'O'
    ROOM_TYPE_CHOICES = (
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (TRIPLE, 'Triple'),
        (QUAD, 'Quad'),
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
    NONE = 'N'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (NONE, 'None'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=NONE,
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
    total_beds = models.PositiveSmallIntegerField(
        default = 0)
    
    # Currently Available Number of Beds
    available_beds = models.PositiveSmallIntegerField(
        default = 0)
    
    # Room Availabilty Status
    available = models.BooleanField(
        default = False)

    class_year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )     #come back to this
    lottery_number = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    ) #come back to this
    
    
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
    NONE = 'N'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (NONE, 'None'),
    )

    Puller_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                                     default=NONE)
    
    Pullee_Number = models.PositiveSmallIntegerField(blank=True, null=True)
    Pullee_Room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name = "Pullee_Room",
        blank=True,
        null=True,
    )

    Pullee_Year = models.PositiveSmallIntegerField(blank = True, null=True)

    FEMALE = 'F'
    MALE = 'M'
    NONE = 'N'
    
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (NONE, 'None'),
    )

    Pullee_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                                     default=NONE)

    def __str__(self):

        toReturn = '#' + str(self.Puller_Number)
        if(self.Pullee_Number == None):
            toReturn += " took a room"
        else:
            toReturn += ' pulled #' + str(self.Pullee_Number)

        return toReturn
