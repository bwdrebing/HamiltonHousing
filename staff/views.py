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
                'form' : form})

def ReviewRoom(request):
    #Allow the user to input a room number to review and edit
        # the information presented

    form = BuildingForm()
    headerText = "Please enter a building and a number to proceed"

    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/RoomSelect.html',
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
    #XXX: Need to extend this to support pulling into different rooms
    #XXX: Need to actually update the available beds in the taken room
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
            form = StudentInfoForm()
            form.init(room.id)
            number = list(LotteryNumber.objects.all())[-1]

            return render(request, 'staff/RoomSelect.html',
            {'HeaderText' : headerText, 
                'Action' : '/staff/RoomSelect/ConfirmSelection',
                'LotteryNumber' : number, 
                'form' : form})

def ConfirmSelection(request):
    #This form will save the transaction based on info of previous form
    #XXX:Need to be able to go back or decline the creation of transactions.
    if request.method == "POST":
        responseForm = StudentInfoForm(request.POST)
        if responseForm.is_valid():
            numberOfStudents = int(request.POST['numOfStudents'])

            #If more than 1 student was involved create a transaction for each
            for i in range(0,numberOfStudents):
                    
                Transaction.objects.create(
                    Puller_Number = request.POST['PullNumber0'],
                    Puller_Year = request.POST['PullYear0'],
                    Puller_Room = Room.objects.get(id=request.POST['PullRoom0']),
                    Puller_Gender = request.POST['PullGender0'],
                    Pullee_Number = request.POST['PullNumber' + str(i)],
                    Pullee_Year = request.POST['PullYear' + str(i)],
                    Pullee_Room = Room.objects.get(id=request.POST['PullRoom' + str(i)]),
                    Pullee_Gender = request.POST['PullGender' + str(i)]
                    )
                
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
