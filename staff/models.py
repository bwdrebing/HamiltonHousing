from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LotteryNumber(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.number)


class Building(models.Model):
    name = models.CharField(max_length = 100)
    total_rooms = models.PositiveSmallIntegerField()
    total_floors = models.PositiveSmallIntegerField()
    total_singles = models.PositiveSmallIntegerField()
    total_doubles = models.PositiveSmallIntegerField()
    total_triples = models.PositiveSmallIntegerField()
    total_quads = models.PositiveSmallIntegerField()
    total_beds = models.PositiveSmallIntegerField()
    location = models.CharField(max_length = 100)
    gender_blocked = models.BooleanField()
    closed = models.BooleanField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    
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
        default = ''
    )
    
    # Notes2 - SPECIFICS2
    notes2 = models.TextField(
        default = ''
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
    
    Pullee_Number = models.PositiveSmallIntegerField(blank=True, null=True)
    Pullee_Room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name = "Pullee_Room",
        blank=True,
        null=True,
    )

    Pullee_Year = models.PositiveSmallIntegerField(blank = True, null=True)

    def __str__(self):

        toReturn = '#' + str(self.Puller_Number)
        if(self.Pullee_Number == None):
            toReturn += " took a room"
        else:
            toReturn += ' pulled #' + str(self.Pullee_Number)

        return toReturn



