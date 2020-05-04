from django.shortcuts import render,redirect,HttpResponse
from .forms import LocationForm
from .models import Location
import requests

# Create your views here.
def index(request):
    return render(request,'track/index.html',{})

def tes(request):
    url='https://api.rootnet.in/covid19-in/stats/latest'
    r=requests.get(url).json()
    print(r)
    out=r['data']['regional']
    context={'out': out } 
    return render(request,'track/tes.html',context)

def tracker(request):
    n = Location.objects.all()
    if request.method == "POST":
        form = LocationForm(request.POST)
        rr=True
        if form.is_valid():
            url= 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2edc88045665cd7d7e9ce52053e0948a'
            city=(request.POST.get("Country"))
            r = requests.get(url.format(city)).json()

            if len(r) == 2:
                if r['message']=='city not found':
                    return HttpResponse("Not Found")
            al = []
            for i in n:
                if str(i.Country) == str(city):
                    rr=False
            if rr==True:
                form.save()
                n=Location.objects.all()
            for i in n:
                r = requests.get(url.format(i.Country)).json()
                print(r)
                w_d = {
                    'city' : i.Country,
                    'temperature' : r['main']['temp'],
                    'icon' : r['weather'][0]['icon'],
                    'description' : r['weather'][0]['description']
                }
                al.append(w_d)
            print (al)
            print(r)
            form = w_d
            return render(request,'track/result.html',{'al':al})
    else:
        form = LocationForm()
    return render(request, 'track/tracker.html', {'form': form})