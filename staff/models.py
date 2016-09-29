from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Building(models.Model):
    name = models.CharField(max_length = 100, primary_key = true)
    totalRooms = models.PositiveSmallIntegerField()
    totalFloors = models.PositiveSmallIntegerField()
    totalSingles = models.PositiveSmallIntegerField()
    totalDoubles = models.PositiveSmallIntegerField()
    totalTriples = models.PositiveSmallIntegerField()
    totalQuads = models.PositiveSmallIntegerField()
    totalBeds = models.PositiveSmallIntegerField()
    location = models.CharField(max_length = 100)
    genderBlocked = models.BooleanField()
    closed = models.BooleanField()
    notes = models.TextField()
    
    def __str__(self):

        return self.name
    
