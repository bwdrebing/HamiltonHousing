from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from .models import LotteryNumber 
from .models import Building
from .models import Room
from .models import Transaction
from .models import BlockTransaction
from .models import Resident
from .models import StaffPageContent

from .forms import *

@login_required
def lotteryNumberInput(request):
    """View with a simple form that allows a new Next Lottery Number to be input"""
    if request.method == "POST":
        form = LotteryNumberForm(request.POST)
        if form.is_valid():
            form.save()

    #fixme: Change so lottery number doesn't load if there is none
    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    form = LotteryNumberForm()
    return render(request, 
                  'staff/LotteryNumberInput.html', 
                  {'LotteryNumber': number,'form' : form})

@login_required
def RoomSelect(request):
    """Sends a form to request a building name and room number. Redirect to the StudentInfo to render    a new form"""
    form = BuildingForm()
    
    headerText = "Please enter room information to get started..."

    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    
    return render(request, 
                  'staff/select/room.html',
                  {'HeaderText' : headerText,
                   'Action': reverse('room-select-student-info'),
                   'LotteryNumber' : number,
                   'rooms' : list(Room.objects.all()),
                   'form' : form})

@login_required
def suiteSelect(request):
    """Select a suite as a living space - almost exactly room select"""
    form = suiteInfoForm()
    headerText = "Select the suite you are trying to fill..."
    suites = Room.objects.filter(room_type = 'B').exclude(available = False) # get all block rooms
    
    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    
    #fixme: Only render available rooms
    return render(request,
                  'staff/select/suite.html',
                  {'headerText': headerText,
                   'Action': reverse('suite-select-student-info'),
                   'LotteryNumber': number,
                   'form': form,
                   'suites': suites})

@login_required
def ReviewRoom(request):
    """Allow the user to input a room number to review and edit the information presented"""
    form = BuildingForm()
    headerText = "Please enter a building and a number to proceed"

    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    return render(request, 
                  'staff/edit/transaction.html',
                  {'HeaderText' : headerText,
                   'Action' : reverse('review-room-student-info'),
                   'LotteryNumber' : number,
                   'form' : form})

@login_required
def ReviewStudentInfo(request):
    """Allows a staff user to view edit the student info in a transaction"""
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
            number = list(LotteryNumber.objects.all())
            if(number):
                number = number[-1]
            else:
                number = ""
        
            return render(request, 
                          'staff/edit/transactionStudentInfo.html',
                          {'HeaderText' : headerText, 
                           'Action' : reverse('review-room-confirm'),
                           'LotteryNumber' : number, 
                           'form' : form})

@login_required
def StudentInfo(request):
    """Gather information about student and any roommates they might have"""
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
            print(room.pull)
            if(room.pull != '' and rooms.get(number = room.pull).available == True):
                additionalForm = StudentInfoForm()
                pullRoom = rooms.get(number = room.pull)
                roomsToRender.append(pullRoom)
                additionalForm.forAdditionalRoom(pullRoom)
                formsToRender.append(additionalForm)
            
            headerText = "Placing student in  " + \
                str(responseForm.cleaned_data['name']) + \
                " " + str(responseForm.cleaned_data['room_number'])
           

            number = list(LotteryNumber.objects.all())
            if(number):
                number = number[-1]
            else:
                number = ""
        

            return render(request,
                          'staff/select/studentInfo.html',
                          {'HeaderText' : headerText, 
                           'Action' : reverse('room-select-confirm'),
                           'LotteryNumber' : number, 
                           'Rooms' : roomsToRender,
                           'Forms' : formsToRender})

@login_required
def suiteStudentInfo(request):
    """Step 2 of the suite selection process - allows a user to input information about the students being placed in a suite during the blocking lottery"""
    if request.method == "POST":
        responseForm = suiteInfoForm(request.POST)
        if responseForm.is_valid():
            building = Building.objects.get(
            name = responseForm.cleaned_data['building'])

            rooms = Room.objects.filter(building = building)
            room = rooms.get(number = responseForm.cleaned_data['suite_number'])

            roomsToRender = [room]

            baseForm = StudentInfoForm()
            baseForm.forBlock(room)

            formsToRender = [baseForm]
            
            headerText = "Placing student in  " + \
                str(responseForm.cleaned_data['building']) + \
                " " + str(responseForm.cleaned_data['suite_number'])

            number = list(LotteryNumber.objects.all())
            if(number):
                number = number[-1]
            else:
                number = ""
        
            return render(request, 
                          'staff/select/suiteStudentInfo.html',
                          {'HeaderText' : headerText, 
                           'Action' : reverse('suite-select-confirm'),
                           'LotteryNumber' : number, 
                           'Rooms' : roomsToRender,
                           'Forms' : formsToRender})
        
@login_required
def suiteConfirm(request):
    """A form the show the user the information they input during the suite selection prcoess for confirmation""" 
    #This form will save the transaction based on info of previous form
    #XXX:Need to be able to go back or decline the creation of transactions.
    if request.method == "POST":
        totalNumberOfStudents = int(request.POST['numberOfStudents'])
        
        transaction = BlockTransaction.objects.create(
            block_number = request.POST['blockNumber'],
            suite = Room.objects.get(id=request.POST['Suite'])
        )
        
        for i in range(totalNumberOfStudents):
            resident = Resident.objects.create(
                gender = str(request.POST["Gender" + str(i)])
            )
            transaction.residents.add(resident)
                
        room = Room.objects.get(id=request.POST['Suite'])   
        room.available = False
        room.save()
    
        transaction.save()

    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    
    # todo: when select page is addded action should go there
    return render(request, 
                  'staff/confirmSelection.html',
                  {'HeaderText' : "Confirm Suite Selection Details", 
                   'Action' : reverse('select'),
                   'LotteryNumber' : number, 
                   'form' : None})

@login_required
def ConfirmSelection(request):
    """Shows a user the information they input during the room selection process for confirmation"""
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

    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    return render(request, 
                  'staff/ConfirmSelection.html',
                  {'HeaderText' : "Confirm this Room Selection Please", 
                   'Action' : reverse('room-select'),
                   'LotteryNumber' : number, 
                   'form' : None})

@login_required
def edit(request):
    """A landing page for staff users to see descriptions of the three models they can edit - transactions, rooms, and buildings"""
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    return render(request,
                  'staff/edit/edit.html',
                  {'LotteryNumber' : number})

@login_required
def select(request):
    """A landing page for staff users to see descriptions of the two models they can place selections-
    rooms and suites"""
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    return render(request,
                  'staff/select/select.html',
                  {'LotteryNumber' : number})

@login_required
def editBuilding(request):
    """Displays a form that allows user to edit certain building attributes (closed to women, men, etc.)"""
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    if request.method == "POST":
        #form = editBuildingForm(request.POST, instance = building)
        current_building = Building.objects.get(name=request.POST["building"])
        form = editBuildingForm(request.POST, instance = current_building)
        if form.is_valid():
            form.save()
            return render(request,
                          'staff/edit.html', 
                          {'LotteryNumber': number,'form' : form})
    form = editBuildingForm()
    return render(request, 
                  'staff/edit/building.html', 
                  {'LotteryNumber': number,'form' : form})

@login_required
def editRoom(request):
    """Displays a form that allows user to edit certain room attributes - available, notes, etc."""
    # get next lottery number for header
    nums = list(LotteryNumber.objects.all())
    if (nums):
        number = nums[-1]
    else:
        number = ""
    if request.method == "POST":
        #form = editBuildingForm(request.POST, instance = building)
        current_building = Building.objects.get(name=request.POST["building"])
        current_number = Room.objects.get(name = request.POST["room_number"])
        current_room = [current_building, current_number]
        form = editRoomForm(request.POST, instance = current_room)
        if form.is_valid():
            form.save()
            return render(request,
                          'staff/edit.html', 
                          {'LotteryNumber': number,'form' : form})
    form = editRoomForm()
    return render(request, 
                  'staff/edit/room.html', 
                  {'LotteryNumber': number,'form' : form})

def userLogin(request):
    if not request.user.is_authenticated:
        number = list(LotteryNumber.objects.all())
        if(number):
            number = number[-1]
        else:
            number = ""

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':
            print("iN LOGIN POST SECTION")
            # Gather the username and password provided by the user
            username = request.POST['username']
            password = request.POST['password']

            # see if combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            # If we have a User object, the details are correct.
            if user:

                print("found user object")
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # We'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect(reverse('staff-home'))
                else:
                    # An inactive account was used - no logging in!
                    # fixme: make this better (httpresponse)
                    return HttpResponse("Your Staff account is disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                # fixme: delete this when we know its working
                print("Invalid login details: {0}, {1}".format(username, password))
                return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
        else:
            login_form = userLoginForm()
            return render(request,
                          'staff/login.html',
                          {'LotteryNumber' : number,
                           'login_form': login_form})
    else:
        return HttpResponseRedirect(reverse('staff-home'))
    
@login_required
def userLogout(request):
     # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('staff-home'))
    
@login_required
def home(request):
    """The home page"""
    number = list(LotteryNumber.objects.all())
    if(number):
        number = number[-1]
    else:
        number = ""
        
    pageContent = StaffPageContent.objects.filter(active=True)
    if (pageContent):
        pageContent = pageContent.latest()
    else:
        pageContent = ""
        
    return render(request, 
                  'staff/home.html',
                  {'LotteryNumber' : number,
                   'pageContent': pageContent})