from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import *

import re

# All the variations of building types to be removed to ensure uniformity
HouseSyns = ['apts', 'apt', 'apartment', 'apartments', 'house', 'hall', 'estate', 'dorm', 'dormitory'] #what if Wally J? fix later...

# -------------------------------------------------------------
#   ROOM ADMIN MODEL
# -------------------------------------------------------------

# Resource for importing rooms through an excel spreadsheet
class RoomResource(resources.ModelResource):
    building = fields.Field(
        attribute = 'building', 
        column_name = 'BUILDING', 
        widget = ForeignKeyWidget(Building, 'name'))
    number = fields.Field(
        attribute = 'number', 
        column_name = 'ROOM')
    room_type = fields.Field(
        attribute = 'room_type', 
        column_name = 'ROOM TYPE', 
        default = 'O')
    gender = fields.Field(
        attribute = 'gender', 
        column_name = 'GENDER', 
        default = 'E')
    pull = fields.Field(
        attribute = 'pull', 
        column_name = 'PULL', 
        default = '') 
    apartment = fields.Field(
        column_name = 'APARTMENT')
    notes = fields.Field(
        attribute = 'notes', 
        column_name = 'SPECIFICS', 
        default = '')
    notes2 = fields.Field(
        attribute = 'notes2', 
        column_name = 'SPECIFICS2', 
        default = '')
    
    class Meta:
        import_id_fields = ['building', 'number']
        model = Room
        fields = ('building', 'number', 'room_type', 'gender', 'pull', 'notes', 'notes2',                       'apartment')
        export_order = fields
        
    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """

        row['BUILDING'] = str(row['BUILDING'])
        for key, value in row.items():
            if isinstance(value, str):
                row[key] = re.sub('[^A-Za-z0-9 ]+', '', row[key])
            if (value == "DOUBLE"):
                row[key] = 'D'
            if (value == "SINGLE"):
                row[key] = 'S'
            if (value == "TRIPLE"):
                row[key] = 'T'
            if (value == "QUAD"):
                row[key] = 'Q'
            if (value == "EITHER"):
                row[key] = 'E'
            if (value == "FEMALE"):
                row[key] = 'F'
            if (value == "MALE"):
                row[key] = 'M'
            
            if isinstance(row[key], str):
                row[key] = row[key].strip()
                for word in row[key].split():
                    if word.lower() in HouseSyns:
                        row[key] = row[key].replace(' '+ word, '', 1)
        # if this room is in an apartment
        if (row['APARTMENT']):
            
            # check if the apartment already exists, otherwise make it
            bldg = Building.objects.get(name = row['BUILDING'])    
            print(bldg)
            apt = (Apartment.objects.filter(building = bldg)
                                    .filter(number = row['APARTMENT']))    

            if (not apt):
                apt = Apartment.objects.create_apartment(bldg, row['APARTMENT'])
                
            row['APARTMENT'] = (Apartment.objects.filter(building = bldg)
                                                 .get(number = row['APARTMENT']))  

    def after_import_row(self, row, row_result, **kwargs):   
        instanceBuilding = Building.objects.get(name = row['BUILDING'])
        instance = Room.objects.filter(building = instanceBuilding).get(number = row['ROOM'])
        if(row['ROOM TYPE'] == "S"):
            instance.total_beds = 1
        if(row['ROOM TYPE'] == "D"):
            instance.total_beds = 2
        if(row['ROOM TYPE'] == "T"):
            instance.total_beds = 3
        if(row['ROOM TYPE'] == "Q"):
            instance.total_beds = 4
        if(row['ROOM TYPE'] == "B"):
            instance.total_beds = 6
        
        instance.available_beds = instance.total_beds
        instance.available = True
        
        # add apartment if it exists
        if (row['APARTMENT']):
            instance.apartment = row['APARTMENT']
            
        instance.save()
        
        """ Would like to add this but not sure if it will break room select
        
        def after_import(dataset, result, using_transactions, dry_run, **kwargs):
        # fixme: make after import to add pulls
        for row in dataset:
            if row['pull']:
                bldg = Building.objects.get(name = row['BUILDING'])
                room = Room.objects.filter(building = bldg).get(number = row['ROOM'])
                pull = Room.objects.filter(building = bldg).get(number = row['PULL'])
                if (pull):
                    room.pull = pull
                    room.save()"""
        
      
# Action for admin page
def make_room_available(modeladmin, request, queryset):
    """Adds action to Room admin page - make rooms available"""
    queryset.update(available=True)

# Action for admin page
def make_room_unavailable(modeladmin, request, queryset):
    """Adds action to Room admin page - make rooms unavailable"""
    queryset.update(unavailable=True)
    
# Action for admin page (not sure if this will be useful for the future
def make_all_beds_available(modeladmin, request, queryset):
    """Adds action to Room admin page - make available beds equal to total number of beds"""
    for entry in queryset:
        entry.available_beds = entry.total_beds
        entry.save()

# admin action descriptions
make_room_available.short_description = "Mark selected rooms as available"
make_room_unavailable.short_description = "Mark selected rooms as unavailable"
make_all_beds_available.short_description = "Make all beds available for selected rooms"

class RoomAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RoomResource
    list_display = ['building', 'number', 'room_type', 'apartment', 'available_beds', 'gender',                       'available']
    list_filter = ('gender', 'apartment', 'building')
    ordering = ['building']
    actions = [make_room_available, make_room_unavailable, make_all_beds_available]
    
# Resource for importing buildings using an excel spreadsheet

# -------------------------------------------------------------
#   BUILDING ADMIN MODEL
# -------------------------------------------------------------
class BuildingResource(resources.ModelResource):
    name = fields.Field(
        attribute = 'name', 
        column_name = 'Building')
    total_singles = fields.Field(
        attribute = 'total_singles', 
        column_name = '# Singles')
    total_doubles = fields.Field(
        attribute = 'total_doubles', 
        column_name = '# Doubles')
    total_triples = fields.Field(
        attribute = 'total_triples', 
        column_name = '# Triples')
    total_quads = fields.Field(
        attribute = 'total_quads', 
        column_name = '# Quads')
    total_fivepulls = fields.Field(
        attribute = 'total_fivepulls', 
        column_name = '#5-Pulls')
    total_sixpulls = fields.Field(
        attribute = 'total_sixpulls', 
        column_name = '#6-Pulls')
    total_rooms = fields.Field(
        attribute = 'total_rooms', 
        column_name = 'Total # Rooms')
    total_beds = fields.Field(
        attribute = 'total_beds', 
        column_name = 'Capacity')
    
    class Meta:
        import_id_fields = ['name']
        model = Building
        fields = ('name', 'total_singles', 'total_doubles', 'total_triples', 'total_quads', 'total_fivepulls', 'total_sixpulls', 'total_rooms', 'total_beds')
        export_order = fields
        
    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        for key, value in row.items():
            if (value):
                row[key] = re.sub('\s*\([^\)]+\)', '', row[key])
                row[key] = re.sub('[^A-Za-z0-9 ]+', '', row[key])
                
                #Convert building name to a string to preprocess it
                if (key == u'Building'):
                    row[key] = str(row[key]) 

                if isinstance(row[key], str):
                    row[key] = row[key].strip()
                    for word in row[key].split():
                        if word.lower() in HouseSyns:
                            row[key] = row[key].replace(' '+ word, '', 1)
            if (row[key] == ''):
                row[key] = 0

    def after_import_row(self, row, row_result, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        for key, value in row.items():
            if isinstance(row[key], str):
                if ('Total' in value):
                    Building.objects.get(name = value).delete()

# MASS MAKE UNAVAILABLE ACTION FOR ADMIN PAGE
def make_buildings_unavailable(modeladmin, request, queryset):
    """Adds action to Building admin page - make buildings unavailable"""
    queryset.update(available=False)
   
# Mass action for admin page
def make_buildings_available(modeladmin, request, queryset):
    """Adds action to Building admin page - make buildings available"""
    queryset.update(available=True)    
    
# admin action descriptions
make_buildings_unavailable.short_description = "Mark selected buildings as unavailable"
make_buildings_available.short_description = "Mark selected buildings as available"
        
class BuildingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BuildingResource
    list_display = ['name', 'total_rooms', 'closed_to', 'available']
    ordering = ['name']
    
    # fixme: add more options? what are good filtering options
    list_filter = ('closed_to', )
    actions = [make_buildings_available, make_buildings_unavailable]

    
# Register models on Admin site

# -------------------------------------------------------------
#   TRANSACTION ADMIN MODEL
# -------------------------------------------------------------

class TransactionResource(resources.ModelResource):
    '''this is just the bare bones set up for exporting transactions
    after we adjust this model we can set up export processing with
    foreignkeys, nice titles, etc'''
    
    class Meta:
        model = Transaction
        
class TransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TransactionResource
    
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['building', 'number', 'gender']
    ordering = ['building', 'number']
    
# MASS MAKE UNAVAILABLE ACTION FOR ADMIN PAGE
def make_contents_unavailable(modeladmin, request, queryset):
    """Make buildings unavailable"""
    queryset.update(available=False)
   
# Mass action for admin page
def make_contents_available(modeladmin, request, queryset):
    """Make buildings available"""
    queryset.update(available=True)    
    
# admin action descriptions
make_contents_unavailable.short_description = "Mark selected contents as unavailable"
make_contents_available.short_description = "Mark selected contents as available"
    
class StaffPageContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'lottery_name', 'header_text', 'updated', 'active']
    actions = [make_contents_available, make_contents_unavailable]
        
admin.site.register(LotteryNumber)
admin.site.register(FloorPlan)
admin.site.register(BlockTransaction)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Building, BuildingAdmin)    
admin.site.register(Room, RoomAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(StaffPageContent, StaffPageContentAdmin)
