from django import forms

from .models import LotteryNumber
from .models import Building

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number',)

class BuildingForm(forms.Form):
    
    name = forms.ChoiceField(
                choices = [(str(o), str(o)) for o in list(Building.objects.all())])

    room_number = forms.CharField()

class StudentInfoForm(forms.Form):

    def __init__(self, num_students):
        super(StudentInfoForm, self).__init__()
        for i in range(1,num_students + 1):
            self.fields['Resident #' + str(i) + ' Lottery Number'] = forms.IntegerField()
            
            self.fields['Resident #' + str(i) + ' Gender'] = forms.ChoiceField(
                choices = [('male', 'Male'), ('female', 'Female')] 
                )

            self.fields['Resident #' + str(i) + ' Class Year'] = forms.ChoiceField(
                choices = [(num, num) for num in range (2014, 2019)]
                )
