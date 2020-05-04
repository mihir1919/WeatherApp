from django.shortcuts import render,redirect
from .forms import LocationForm
import requests

# Create your views here.
def index(request):
    return render(request,'track/index.html',{})

def tracker(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            url= 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2edc88045665cd7d7e9ce52053e0948a'
            city=(request.POST.get("Country"))
            r = requests.get(url.format(city)).json()
            print(r)
            form = r
            return render(request,'track/result.html',{'form':form})
    else:
        form = LocationForm()
    return render(request, 'track/tracker.html', {'form': form})