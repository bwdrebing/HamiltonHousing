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

    def forBaseRoom(self, room, prefix = ""):
        self.numberOfStudents = room.available_beds
        self.fields[prefix + 'numberOfStudents'] = forms.IntegerField( 
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
                )
        for i in range(self.numberOfStudents):

            self.fields[prefix + 'Room' + str(i)] = forms.IntegerField(
                    initial = room.id,
                    widget = forms.HiddenInput(),
                )
            
            self.fields[prefix + 'Room_Number' + str(i)] = forms.CharField(
                    disabled = True,
                    initial = room.number 
                )

            self.fields[prefix + 'Number' + str(i)] = forms.IntegerField(
                    label = 'Resident #' + str(i+1) + ' Lottery Number')
           

            self.fields[prefix + 'Year'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (2014, 2019)]
                )

            self.fields[prefix + 'Gender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('male', 'Male'), ('female', 'Female')] 
                )

    def forAdditionalRoom(self, room):
        self.fields['Show_Pull'] = forms.BooleanField(
                label = "Pulling Someone",
                required = False,
                initial = True)
        self.forBaseRoom(room, "Pull")


