from django.shortcuts import render,redirect
from .forms import LocationForm
from .models import Location
import requests

# Create your views here.
def index(request):
    return render(request,'track/index.html',{})

def tracker(request):
    n = Location.objects.all()
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.POST.get("Country") not in n:
            form.save()
        if form.is_valid():
            url= 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2edc88045665cd7d7e9ce52053e0948a'
            city=(request.POST.get("Country"))
            r = requests.get(url.format(city)).json()
            w_d = {
                'city' : city,
                'temperature' : r['main']['temp'],
                'icon' : r['weather'][0]['icon'],
                'description' : r['weather'][0]['description']
            }
            print(r)
            form = w_d
            return render(request,'track/result.html',{'form':form,'n':n})
    else:
        form = LocationForm()
    return render(request, 'track/tracker.html', {'form': form})