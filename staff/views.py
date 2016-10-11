from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from .models import LotteryNumber 
from .models import Building

from .forms import LotteryNumberForm
from .forms import BuildingForm

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
    if request.method == "POST":
        form = BuildingForm(request.POST)
        if form.is_valid:
           print("Building Chosen")
           #Do some redirection here
    form = BuildingForm()
    buildings = list(Building.objects.all())
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/RoomSelect.html',
            {'buildings' : buildings, 'LotteryNumber' : number, 'form' : form})

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render(request, 'staff/UploadForms.html', {'form': form}, context_instance=RequestContext(request))


def home(request):
    number = list(LotteryNumber.objects.all())[-1]
    return render(request, 'staff/home.html',
                {'LotteryNumber' : number})
