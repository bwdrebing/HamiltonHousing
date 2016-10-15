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
admin.site.register(Building)
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
        

        
class RoomAdmin(ImportExportModelAdmin):
    resource_class = RoomResource
    
admin.site.register(Room, RoomAdmin)
    
