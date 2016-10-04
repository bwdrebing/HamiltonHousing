from django import forms

from .models import LotteryNumber
from .models import Building

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number',)

class BuildingForm(forms.Form):
    
    name = forms.ChoiceField(
                choices = [(o.id, str(o)) for o in list(Building.objects.all())])
    lottery_Number = forms.IntegerField()
    genderChoices = [("F","Female"),("M","Male")]
    gender = forms.ChoiceField(choices=genderChoices)
