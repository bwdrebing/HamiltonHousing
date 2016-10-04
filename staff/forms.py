from django import forms

from .models import LotteryNumber
from .models import Building

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number',)

class BuildingForm(forms.Form):

    #maybe just keep the id as first thing in tuple below
    name = forms.ChoiceField(
                choices = [(str(o), str(o)) for o in list(Building.objects.all())])
    room_number = forms.IntegerField()


class StudentInfoForm(forms.Form):

    lottery_number = forms.IntegerField()

    gender_choices = [('male', 'Male'), ('female', 'Female')]

    gender = forms.ChoiceField(
        choices = gender_choices
    )

    year_choices = [(num, num) for num in range(2014, 2019)]
    
    class_year = forms.ChoiceField(choices = year_choices)
