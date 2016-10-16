from django.contrib import admin
from .models import LotteryNumber
from .models import Building
from .models import Room
from .models import Transaction
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import *

#from core.models import Room

admin.site.register(LotteryNumber)
#admin.site.register(Building)
admin.site.register(Transaction)
#admin.site.register(Room)



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
    
    #def dehydrate_room_name(self, Room):
       # return '%s'
        
    #def after_import_instance(instance, new, **kwargs):
    
    rows = {'BUILDING', 'ROOM', 'ROOM TYPE', 'GENDER', 'PULL', 'SPECIFICS1', 'SPECIFICS2'}
    
    def before_import_rows(rows, **kwargs):
        print("TESTING BEFORE IMPORT ROWS")
        
        

        
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
        
        
    # row = {'Building', '# Singles', '# Doubles', '# Triples', '# Quads', 'Total # Rooms', 'Capacity'}
        
    #def before_import_row(row, **kwargs):
        #print("TESTING BEFORE_IMPORT_ROW")
        
    
        
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource

    
admin.site.register(Building, BuildingAdmin)    
admin.site.register(Room, RoomAdmin)
    
