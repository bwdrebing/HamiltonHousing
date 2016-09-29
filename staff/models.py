from __future__ import unicode_literals

from django.db import models

# Create your models here.

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
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length = 5)
    total_rooms = models.PositiveSmallIntegerField()
    
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
    
    available = models.BooleanField()
    available_beds = models.PositiveSmallIntegerField()
    total_beds = models.PositiveSmallIntegerField()
    pull = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
    )
    
    class_year = models.PositiveSmallIntegerField()     #come back to this
    lottery_number = models.PositiveSmallIntegerField() #come back to this
    
    def __str__(self):
        return (self.building + self.number)