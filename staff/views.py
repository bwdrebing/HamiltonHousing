from django.shortcuts import render
from .models import Building

#Create your views here.
def home(request):
    buildings = list(Building.objects.all())
    return render(request, 'staff/home.html', {'buildings': buildings})
