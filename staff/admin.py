from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import *

import re
import difflib

admin.site.register(LotteryNumber)
admin.site.register(FloorPlan)
admin.site.register(Transaction)

HouseSyns = ['apts', 'apt', 'apartment', 'apartments', 'house', 'hall', 'estate', 'dorm', 'dormitory'] #what if Wally J? fix later...

class RoomResource(resources.ModelResource):
    building = fields.Field(attribute = 'building', column_name = 'BUILDING', widget = ForeignKeyWidget(Building, 'name'))
    number = fields.Field(attribute = 'number', column_name = 'ROOM')
    room_type = fields.Field(attribute = 'room_type', column_name = 'ROOM TYPE')
    gender = fields.Field(attribute = 'gender', column_name = 'GENDER')
    pull = fields.Field(attribute = 'pull', column_name = 'PULL', default = '') 
        #we are only using number as an id because we know it has to pull within the same building
    notes = fields.Field(attribute = 'notes', column_name = 'SPECIFICS', default = '')
    notes2 = fields.Field(attribute = 'notes2', column_name = 'SPECIFICS2', default = '')
    
    class Meta:
        import_id_fields = ['number']
        model = Room
        fields = ('building', 'number', 'room_type', 'gender', 'pull', 'notes', 'notes2')
        export_order = fields
        
    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        for key, value in row.items():
            if(value):
                row[key] = re.sub('[^A-Za-z0-9 ]+', '', value)
            if (value == "DOUBLE"):
                row[key] = 'D'
            if (value == "SINGLE"):
                row[key] = 'S'
            if (value == "TRIPLE"):
                row[key] = 'T'
            if (value == "QUAD"):
                row[key] = 'Q'
            if (value == "EITHER"):
                row[key] = 'N'
            if (value == "FEMALE"):
                row[key] = 'F'
            if (value == "MALE"):
                row[key] = 'M'
            
            if(isinstance(row[key], str)):
                row[key] = row[key].strip()
                for word in row[key].split():
                    if word.lower() in HouseSyns:
                        row[key] = row[key].replace(' '+ word, '', 1)
                        
class RoomAdmin(ImportExportModelAdmin):

    resource_class = RoomResource
    
class BuildingResource(resources.ModelResource):
    name = fields.Field(attribute = 'name', column_name = 'Building')
    total_singles = fields.Field(attribute = 'total_singles', column_name = '# Singles')
    print(type(total_singles))
    total_doubles = fields.Field(attribute = 'total_doubles', column_name = '# Doubles')
    total_triples = fields.Field(attribute = 'total_triples', column_name = '# Triples')
    total_quads = fields.Field(attribute = 'total_quads', column_name = '# Quads')
    total_rooms = fields.Field(attribute = 'total_rooms', column_name = 'Total # Rooms')
    total_beds = fields.Field(attribute = 'total_beds', column_name = 'Capacity')
    
    class Meta:
        import_id_fields = ['name']
        model = Building
        exclude = ('#5-Pulls','#6-Pulls')
        fields = ('name', 'total_singles', 'total_doubles', 'total_triples', 'total_quads', 'total_rooms', 'total_beds')
        export_order = fields
        
    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        for key, value in row.items():
            if(value):
                row[key] = re.sub('\s*\([^\)]+\)', '', row[key])
                row[key] = re.sub('[^A-Za-z0-9 ]+', '', row[key])
                if(isinstance(row[key], str)):
                    row[key] = row[key].strip()
                    for word in row[key].split():
                        if word.lower() in HouseSyns:
                            row[key] = row[key].replace(' '+ word, '', 1)
                        
            if(row[key] == ''):
                row[key] = 0

    def after_import_row(self, row, row_result, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        
        for key, value in row.items():
            if(isinstance(row[key], str)):
                if('Total' in value):
                    Building.objects.get(name = value).delete()
                    
                    
        
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource

    
admin.site.register(Building, BuildingAdmin)    
admin.site.register(Room, RoomAdmin)
    
