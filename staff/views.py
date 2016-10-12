from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from .models import LotteryNumber 
from .models import Building
from .models import Room

from .forms import LotteryNumberForm
from .forms import BuildingForm
from .forms import StudentInfoForm

from django import forms
import django_excel as excel
from django.http import HttpResponseBadRequest, HttpResponse
from django.template import RequestContext

#Form to upload excel spreadsheets
class UploadFileForm(forms.Form):
    file = forms.FileField()
    
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

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render(request, 'staff/UploadForms.html', {'form': form}, context_instance=RequestContext(request))

'''
def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[Room],
                initializers=[None],
                mapdicts=[
                    ['building', 'number', 'room_type', 'gender', 'pull', 'notes', 'notes2']]
            )
            
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'staff/ImportForms.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })
'''

def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=1,
                model=Room,
                mapdict=['BUILDING': 'building', 'ROOM': 'number', 'ROOM TYPE': 'room_type', 'GENDER': 'gender', 'PULL': 'pull', 'SPECIFIC1': 'notes', 'SPECIFIC1': 'notes2'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'staff/ImportForms.html',
        {'form': form})


def home(request):
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/home.html',
                {'LotteryNumber' : number})
