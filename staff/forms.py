from django import forms
from .models import LotteryNumber
from .models import Building
from .models import Room

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number',)

class BuildingForm(forms.Form):
    
    name = forms.ChoiceField(
                choices = [(str(o), str(o)) for o in list(Building.objects.all())])

    room_number = forms.CharField()

class StudentInfoForm(forms.Form):
    numberOfStudents = 0

    def init(self, chosenRoomID):
        self.numberOfStudents = Room.objects.get(id=chosenRoomID).available_beds
        self.fields['numOfStudents'] = forms.IntegerField( 
                initial = self.numberOfStudents, 
                widget = forms.HiddenInput(),
                )
        for i in range(self.numberOfStudents):

            self.fields['PullNumber' + str(i)] = forms.IntegerField(
                    label = 'Resident #' + str(i+1) + ' Lottery Number')
           
            self.fields['PullRoom' + str(i)] = forms.IntegerField(
                    initial = chosenRoomID,
                    widget = forms.HiddenInput(),
                )

            self.fields['PullYear'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (2014, 2019)]
                )

            self.fields['PullGender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('male', 'Male'), ('female', 'Female')] 
                )


