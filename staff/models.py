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
    pull = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    # Total Number of Beds in Room
    total_beds = models.PositiveSmallIntegerField()
    
    # Currently Available Number of Beds
    available_beds = models.PositiveSmallIntegerField()
    
    # Room Availabilty Status
    available = models.BooleanField()



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
        blank=True
    )
    
    # Notes2 - SPECIFICS2
    notes2 = models.TextField(
        blank=True
    )
    
    def __str__(self):
        return (str(self.building) + " " + str(self.number))
