from django import forms
from .models import LotteryNumber
from .models import Building
from .models import Room
from .models import Transaction

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number',)

class BuildingForm(forms.Form):
    name = forms.ChoiceField()
    room_number = forms.ChoiceField()
    
    def __init__(self, *args, **kargs):
        super(BuildingForm, self).__init__(*args, **kargs)
        
        buildingChoices = [(o.name, o.name) for o in list(Building.objects.all())]
        buildingChoices.insert(0,('','-- Select a Building --')) 

        rooms = list(Room.objects.filter(available=True).exclude(available_beds = 0))
        roomChoices = [(o.number, o.building) for o in rooms]
        
        self.fields['name'].choices = buildingChoices 
        self.fields['room_number'].choices = roomChoices
        
class suiteInfoForm(forms.Form):
    """A form allowing a user to choose a building and room number that corresponds to a block"""
    building = forms.ChoiceField()
    suite_number = forms.ChoiceField()
    
    def __init__(self, *args, **kargs):
        kargs.setdefault('label_suffix', '')
        super(suiteInfoForm, self).__init__(*args, **kargs)
        blocks = list(Room.objects.filter(available = True)
                                  .exclude(available_beds = 0)
                                  .filter(room_type = 'B'))
        
        suiteChoices = []
        buildingChoices = []
        
        for block in blocks:
            suiteChoices.append((block.number, block.building))
            if (block.building.name, block.building.name) not in buildingChoices:
                buildingChoices.append((block.building.name, block.building.name))
    
        buildingChoices.insert(0,('','-- Select a Building --')) 
        
        self.fields['building'].choices = buildingChoices 
        self.fields['suite_number'].choices = suiteChoices
        
    
class StudentInfoForm(forms.Form):
    numberOfStudents = 0

    def forBlock(self, suite, prefix=""):
        self.numberOfStudents = suite.available_beds
        self.fields[prefix + 'numberOfStudents'] = forms.IntegerField( 
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
        )
        
        self.fields[prefix + 'Number0'] = forms.IntegerField(label = 'Block Lottery Number')

        for i in range(self.numberOfStudents):
            self.fields[prefix + 'Suite_Number' + str(i)] = forms.CharField(
                    disabled = True,
                    initial = suite.number,
                    widget = forms.HiddenInput()
            )
            
            self.fields[prefix + 'Room' + str(i)] = forms.IntegerField(
                    initial = suite.id,
                    widget = forms.HiddenInput(),
            )
            
            self.fields[prefix + 'Gender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('M', 'Male'), ('F', 'Female')] 
            )

    
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
                    initial = room.number,
                    widget = forms.HiddenInput()
                )

            self.fields[prefix + 'Number' + str(i)] = forms.IntegerField(
                    label = 'Resident #' + str(i+1) + ' Lottery Number')
           

            self.fields[prefix + 'Year'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (2014, 2019)]
                )

            self.fields[prefix + 'Gender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('M', 'Male'), ('F', 'Female')] 
                )

    def forAdditionalRoom(self, room):
        self.fields['Show_Pull'] = forms.BooleanField(
                label = "Pulling Someone",
                required = False,
                initial = True)
        self.forBaseRoom(room, "Pull")


class ReviewStudentInfoForm(forms.Form):
    numberOfStudents = 0

    def init(self, chosenRoomID):
        room = Room.objects.get(id=chosenRoomID)
        transaction_rooms = Transaction.objects.filter(Pullee_Room = 
                                                           room)
        self.numberOfStudents = transaction_rooms.count()

        self.fields['numberOfStudents'] = forms.IntegerField( 
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
                )
        for i in range(self.numberOfStudents):

            self.fields['Number' + str(i)] = forms.IntegerField(
                    label = 'Resident #' + str(i+1) + ' Lottery Number', 
                    initial = transaction_rooms[i].Pullee_Number)
           
            self.fields['Room' + str(i)] = forms.IntegerField(
                    initial = chosenRoomID,
                    widget = forms.HiddenInput(),
                )

            self.fields['Year'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (2014, 2019)],
                initial = transaction_rooms[i].Pullee_Year
                )

            self.fields['Gender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('male', 'Male'), ('female', 'Female')],
                initial = transaction_rooms[i].Pullee_Year
                )
