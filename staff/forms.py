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

        rooms = list(Room.objects.filter(available=True))
        roomChoices = [(o.number, o.building) for o in rooms]
        roomChoices.insert(0,('',''))
        
        self.fields['name'].choices = buildingChoices 
        self.fields['room_number'].choices = roomChoices
        
    
class StudentInfoForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(StudentInfoForm, self).__init__(*args, **kwargs)
        self.numberOfStudents = 0
        self.studentFields = []
        self.pullToggle = None

    def forBlock(self,suite):
        self.numberOfStudents = suite.available_beds
        self.fields[prefix + 'numberOfStudents'] = forms.IntegerField(
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
                )
        self.fields[prefix + 'Number' + str(i)] = forms.IntegerField(
            label = 'Resident #' + str(i+1) + ' Lottery Number')
        

        for i in range(self.numberOfStudents):
            
            #Build field for the room number
            numForm = forms.CharField(
                    disabled = True,
                    initial = suite.number,
                    widget = forms.HiddenInput()
                )
            self.fields[prefix + 'Room_Number' + str(i)] = numForm
            
            
            #Build field for the room id
            roomId = forms.IntegerField(
                    initial = room.id,
                    widget = forms.HiddenInput(),
                )
            self.fields[prefix + 'Room' + str(i)] = roomId
            
            #Build field for student gender
            gender = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('M', 'Male'), ('F', 'Female')] 
                )
            self.fields[prefix + 'Gender'+str(i)] = gender

    
    def forBaseRoom(self, room, prefix = ""):
        self.numberOfStudents = room.available_beds
        self.fields[prefix + 'numberOfStudents'] = forms.IntegerField( 
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
                )
        for i in range(self.numberOfStudents):
            
            self.studentFields.append([])
            
            roomId = forms.IntegerField(
                    initial = room.id,
                    widget = forms.HiddenInput(),
                )
            self.fields[prefix + 'Room' + str(i)] = roomId
            #self.studentFields[i].append(roomId)
            
            roomNumber = forms.CharField(
                    disabled = True,
                    initial = room.number,
                    widget = forms.HiddenInput()
                )
            self.fields[prefix + 'Room_Number' + str(i)] = roomNumber
            #self.studentFields[i].append(roomNumber)
            
            lotteryNumber = forms.IntegerField(
                    label = 'Resident #' + str(i+1) + ' Lottery Number')
            self.fields[prefix + 'Number' + str(i)] = lotteryNumber
            self.studentFields[i].append(self.__getitem__(prefix + 'Number' + str(i)))

            
            classYear = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (2014, 2019)]
                )
            self.fields[prefix + 'Year'+str(i)] = classYear
            self.studentFields[i].append(self.__getitem__(prefix + 'Year' + str(i)))
            
            
            gender= forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('M', 'Male'), ('F', 'Female')] 
                )
            self.fields[prefix + 'Gender'+str(i)] = gender
            self.studentFields[i].append(self.__getitem__(prefix + 'Gender' + str(i)))
            
            
            print(self.fields[prefix + 'Gender' + str(i)].label)
            print(self.studentFields[i][-1].label)
            
    def forAdditionalRoom(self, room):
        self.fields['Show_Pull'] = forms.BooleanField(
                label = "Pulling Someone",
                required = False,
                initial = True)
        self.pullToggle = self.__getitem__('Show_Pull')
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
