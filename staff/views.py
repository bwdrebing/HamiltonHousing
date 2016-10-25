from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from .models import LotteryNumber 
from .models import Building
from .models import Room
from .models import Transaction

from .forms import LotteryNumberForm
from .forms import BuildingForm
from .forms import StudentInfoForm
from .forms import ReviewStudentInfoForm

#Create your views here.
def lotteryNumberInput(request):
    if request.method == "POST":
        form = LotteryNumberForm(request.POST)
        if form.is_valid():
            form.save()

    number = list(LotteryNumber.objects.all())[-1]
    form = LotteryNumberForm()
    return render(request, 'staff/LotteryNumberInput.html', 
            {'LotteryNumber': number,'form' : form})

def RoomSelect(request):
    #Send a form to request a building name and room number
    #Redirect to the StudentInfo to render a new form
    form = BuildingForm()
    headerText = "Please enter student information to get started..."

    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/RoomSelect.html',
            {'HeaderText' : headerText,
                'Action' : '/staff/RoomSelect/StudentInfo',
                'LotteryNumber' : number,
                'rooms' : list(Room.objects.all()),
                'form' : form})

def ReviewRoom(request):
    #Allow the user to input a room number to review and edit
    # the information presented
    form = BuildingForm()
    headerText = "Please enter a building and a number to proceed"

    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/ReviewRoom.html',
            {'HeaderText' : headerText,
                'Action' : '/staff/ReviewRoom/ReviewStudentInfo',
                'LotteryNumber' : number,
                'form' : form})

def ReviewStudentInfo(request):
    if request.method == "POST":
        responseForm = BuildingForm(request.POST)
        if responseForm.is_valid():
            building = Building.objects.get(
                    name = responseForm.cleaned_data['name'])

            rooms = Room.objects.filter(building = building)
            room = rooms.get(number = responseForm.cleaned_data['room_number'])
            
            headerText = "Placing student in  " + \
                str(responseForm.cleaned_data['name']) + \
                " " + str(responseForm.cleaned_data['room_number'])
           
           #Create a form with the room id 
            form = ReviewStudentInfoForm()
            form.init(room.id)
            number = list(LotteryNumber.objects.all())[-1]

            return render(request, 'staff/ReviewRoom.html',
            {'HeaderText' : headerText, 
                'Action' : '/staff/ReviewRoom/ConfirmSelection',
                'LotteryNumber' : number, 
                'form' : form})

def StudentInfo(request):
    #Gather information about student and any roommates they might have
    if request.method == "POST":
        responseForm = BuildingForm(request.POST)
        if responseForm.is_valid():
            building = Building.objects.get(
            name = responseForm.cleaned_data['name'])

            rooms = Room.objects.filter(building = building)
            room = rooms.get(number = responseForm.cleaned_data['room_number'])
            
            roomsToRender = [room]
            
            baseForm = StudentInfoForm()
            baseForm.forBaseRoom(room)
            
            formsToRender = [baseForm]
            
            if(room.pull != '' and rooms.get(number = room.pull).available == True):
                additionalForm = StudentInfoForm()
                pullRoom = rooms.get(number = room.pull)
                roomsToRender.append(pullRoom)
                additionalForm.forAdditionalRoom(pullRoom)
                formsToRender.append(additionalForm)
            
            headerText = "Placing student in  " + \
                str(responseForm.cleaned_data['name']) + \
                " " + str(responseForm.cleaned_data['room_number'])
           

            number = list(LotteryNumber.objects.all())[-1]

            return render(request, 'staff/StudentInfo.html',
            {'HeaderText' : headerText, 
                'Action' : '/staff/RoomSelect/ConfirmSelection',
                'LotteryNumber' : number, 
                'Rooms' : roomsToRender,
                'Forms' : formsToRender})

def StudentInfoForBlock(request):
    if request.method == "POST":
        responseForm = BuildingForm(request.POST)
        if responseForm.is_valid():
            building = Building.objects.get(
            name = responseForm.cleaned_data['name'])

            rooms = Room.objects.filter(building = building)
            room = rooms.get(number = responseForm.cleaned_data['room_number'])

            roomsToRender = [room]

            baseForm = StudentInfoForm()
            baseForm.forBlock(room)

            formsToRender = [baseForm]


            number = list(LotteryNumber.objects.all())[-1]

            return render(request, 'staff/StudentInfo.html',
            {'HeaderText' : headerText, 
                'Action' : '/staff/RoomSelect/ConfirmSelection',
                'LotteryNumber' : number, 
                'Rooms' : roomsToRender,
                'Forms' : formsToRender})

    
def ConfirmSelection(request):
    #This form will save the transaction based on info of previous form
    #XXX:Need to be able to go back or decline the creation of transactions.
    if request.method == "POST":
        totalNumberOfStudents = int(request.POST['numberOfStudents'])

        for i in range(totalNumberOfStudents):
            
            Transaction.objects.create(
                Puller_Number = request.POST['Number0'],
                Puller_Year = request.POST['Year0'],
                Puller_Room = Room.objects.get(id=request.POST['Room0']),
                Pullee_Number = request.POST['Number' + str(i)],
                Pullee_Year = request.POST['Year' + str(i)],
                Pullee_Room = Room.objects.get(id=request.POST['Room' + str(i)]),
                )
            #Update the room in the database
            print(request.POST)
            room = Room.objects.get(id=request.POST['Room' + str(i)])   
            room.gender = str(request.POST["Gender" + str(i)])
            room.lottery_number = int(request.POST["Number0"])
            room.class_year = int(request.POST["Year0"])
            room.available_beds -= 1
            if(room.available_beds == 0):
                room.available = False
            room.save()

        #If a pull wasn't taken, that room should be updated as having no pull
        if('Show_Pull' in request.POST):
            totalNumberOfPulls = int(request.POST['PullnumberOfStudents'])

            for i in range(totalNumberOfPulls):
                
                Transaction.objects.create(
                    Puller_Number = request.POST['Number0'],
                    Puller_Year = request.POST['Year0'],
                    Puller_Room = Room.objects.get(id=request.POST['Room0']),
                    Pullee_Number = request.POST['PullNumber' + str(i)],
                    Pullee_Year = request.POST['PullYear' + str(i)],
                    Pullee_Room = Room.objects.get(id=request.POST['PullRoom' + str(i)]),
                    )
                #Update the room in the database

                room = Room.objects.get(id=request.POST['PullRoom' + str(i)])
                room.lottery_number = request.POST["Number0"]
                room.class_year = request.POST["Year0"]
                room.gender = request.POST["PullGender" + str(i)]
                room.available_beds -= 1
                if(room.available_beds == 0):
                    room.available = False
                room.save()

    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/RoomSelect.html',
            {'HeaderText' : "Confirm this Room Selection Please", 
                'Action' : '/staff/RoomSelect',
                'LotteryNumber' : number, 
                'form' : None})


def home(request):
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/home.html',
                {'LotteryNumber' : number})
