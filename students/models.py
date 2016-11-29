from django.db import models
from staff.models import *

class StudentPageContent(models.Model):
    name = models.CharField(
        max_length=50,
        default="",
        help_text="This is a name for this entry - it will not be displayed"
    )

    header_text = models.CharField(
        max_length=50,
        default="",
        help_text="This text will be displayed on the students home page as a page title",
        verbose_name="Home page main text"
    )

    header_subtext = models.TextField(
        default="",
        help_text="This text will be displayed on the home page below the title in a smaller font",
        verbose_name="Home page lead text"
    )

    lottery_name = models.CharField(
        max_length=25,
        default="",
        help_text="This is the name of the current lottery; it will display on the home page"
    )
    
    contact = models.TextField(
        default='',
        verbose_name="Contact Information",
        help_text="This is a block of text explaining who to contact with any immediate questions."
    )
    
    contact_email = models.CharField(
        max_length=100,
        default='', 
        blank=True,
        help_text="This is the e-mail of the main person to contact with questions."
    )
    
    navbar_announcement = models.TextField(
        max_length=200,
        default='',
        blank=True,
        help_text="This announcement will be displayed in a thin bar below the header navigation bar"
    )

    active = models.BooleanField(default=True)

    navbar_announcement = models.TextField(
        max_length=200,
        default='',
        blank=True,
        help_text="This announcement will be displayed in a thin bar below the header navigation bar"
    )

    updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        get_latest_by = "updated"

    def __str__(self):
        return self.name
