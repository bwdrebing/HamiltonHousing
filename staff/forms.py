from django import forms
from .models import LotteryNumber
from .models import Building
from .models import Room
from .models import Apartment
from .models import Transaction
from django.contrib.auth.models import User

import datetime

class LotteryNumberForm(forms.ModelForm):

    class Meta:
        model = LotteryNumber
        fields = ('number', 'class_year')

class BuildingForm(forms.Form):
    name = forms.ChoiceField()
    room_number = forms.ChoiceField()

    def __init__(self, *args, **kargs):
        super(BuildingForm, self).__init__(*args, **kargs)

        buildings = list(Building.objects.exclude(available=False))
        buildingChoices = [(o.name, o.name) for o in buildings]
        buildingChoices.insert(0,('','-- Select a Building --'))

        apartments = list(Apartment.objects.all())
        apartmentChoices = [("Apartment " + apt.number, apt.building) for apt in apartments]

        rooms = list(Room.objects.filter(available=True, apartment = None).exclude(available_beds = 0))
        rooms = list(Room.objects.filter(available=True)
                                 .exclude(available_beds = 0)
                                 .exclude(room_type = 'B'))

        roomChoices = [(o.number, o.building) for o in rooms]
        roomChoices.insert(0,('',''))

        self.fields['name'].choices = buildingChoices
        self.fields['room_number'].choices = roomChoices + apartmentChoices

class ReviewTransactionForm(forms.Form):
    name = forms.ChoiceField()
    room_number = forms.ChoiceField()

    def __init__(self, *args, **kargs):
        super(ReviewTransactionForm, self).__init__(*args, **kargs)

        buildingChoices = [(o.name, o.name) for o in list(Building.objects.all())]
        buildingChoices.insert(0,('','-- Select a Building --'))


        rooms = list(Room.objects.filter(available=False))
        roomChoices = [(o.number, o.building) for o in rooms]
        roomChoices.insert(0,('',''))

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

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(StudentInfoForm, self).__init__(*args, **kwargs)
        self.numberOfStudents = 0
        self.studentFields = []
        self.pullToggle = None

    def forBlock(self, suite, prefix=""):
        self.numberOfStudents = suite.available_beds
        self.fields[prefix + 'numberOfStudents'] = forms.IntegerField(
                initial = self.numberOfStudents,
                widget = forms.HiddenInput(),
        )

        self.fields[prefix + 'blockNumber'] = forms.IntegerField(label = 'Block Lottery Number')

        #Build field for the room number
        numForm = forms.CharField(
            disabled = True,
            initial = suite.number,
            widget = forms.HiddenInput()
        )

        self.fields[prefix + 'Suite_Number'] = numForm


        #Build field for the room id
        roomId = forms.IntegerField(
            initial = suite.id,
            widget = forms.HiddenInput(),
        )

        self.fields[prefix + 'Suite'] = roomId

        for i in range(self.numberOfStudents):

            self.studentFields.append([])

            #Build field for student gender
            gender= forms.ChoiceField(
                label = 'Gender',
                choices = [('M', 'Male'), ('F', 'Female')]
            )

            self.fields[prefix + 'Gender' + str(i)] = gender
            self.studentFields[i].append(self.__getitem__(prefix + 'Gender' + str(i)))


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

            now = datetime.datetime.now()
            classYear = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (now.year, now.year+5)]
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

            now = datetime.datetime.now()
            self.fields['Year'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Class Year',
                choices = [(num, num) for num in range (now.year, now.year+5)],
                initial = transaction_rooms[i].Pullee_Year
                )

            self.fields['Gender'+str(i)] = forms.ChoiceField(
                label = 'Resident #' + str(i+1) + ' Gender',
                choices = [('male', 'Male'), ('female', 'Female')],
                initial = transaction_rooms[i].Pullee_Year
                )

class editBuildingFormA(forms.Form):
    name = forms.ChoiceField()

    def __init__(self, *args, **kargs):
        super(editBuildingFormA, self).__init__(*args, **kargs)

        buildingChoices = [(o.name, o.name) for o in list(Building.objects.all())]
        buildingChoices.insert(0,('','-- Select a Building --'))

        self.fields['name'].choices = buildingChoices 
        
class editBuildingFormB(forms.ModelForm):        
    class Meta:
        model = Building
        fields = ['name','available', 'closed_to', 'notes']
        widgets = {'name': forms.HiddenInput()}

    
class editRoomFormA(forms.Form):
    name = forms.ChoiceField()
    room_number = forms.ChoiceField()

    def __init__(self, *args, **kargs):
        super(editRoomFormA, self).__init__(*args, **kargs)

        buildingChoices = [(o.name, o.name) for o in list(Building.objects.all())]
        buildingChoices.insert(0,('','-- Select a Building --'))

        rooms = list(Room.objects.all())
        roomChoices = [(o.number, o.building) for o in rooms]
        roomChoices.insert(0,('','-- Select a Room Number --'))

        self.fields['name'].choices = buildingChoices
        self.fields['room_number'].choices = roomChoices
        
class editRoomFormB(forms.ModelForm):        
    class Meta:
        model = Room
        fields = ['building', 'number','available', 'gender', 'available_beds', 'pull', 'notes']
        widgets = {'building': forms.HiddenInput(), 'number': forms.HiddenInput()}
        help_texts = {
            'pull': ('Room number only, do not include building name'),}
    

class userLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kargs):
        super(userLoginForm, self).__init__(*args, **kargs)