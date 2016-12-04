from django.contrib import admin

# Register your models here.
from .models import StudentPageContent, FAQ

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
    
class StudentPageContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'lottery_name', 'header_text', 'updated', 'active']
    actions = [make_contents_available, make_contents_unavailable]
    
class FAQAdmin(admin.ModelAdmin):
    list_display = ['number', 'question']

admin.site.register(StudentPageContent, StudentPageContentAdmin)
admin.site.register(FAQ, FAQAdmin)