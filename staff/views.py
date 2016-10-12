from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from .models import LotteryNumber 
from .models import Building
from .models import Room

from .forms import LotteryNumberForm
from .forms import BuildingForm
from .forms import StudentInfoForm


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
    form = BuildingForm()
    headerText = "Please enter student information to get started..."
    if request.method == "POST":
        responseForm = BuildingForm(request.POST)
        if responseForm.is_valid():
            building = Building.objects.get(name = responseForm.\
                                                cleaned_data['name'])
            rooms = Room.objects.filter(building = building)
            room = rooms.get(number = responseForm.cleaned_data['room_number'])
            
            headerText = "Placing student in  " + \
                str(responseForm.cleaned_data['name']) + \
                " " + str(responseForm.cleaned_data['room_number'])
            form = StudentInfoForm(room.available_beds)


    buildings = list(Building.objects.all())
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/RoomSelect.html',
            {'HeaderText' : headerText, 'LotteryNumber' : number, 'form' : \
                 form})



def home(request):
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/home.html',
                {'LotteryNumber' : number})
