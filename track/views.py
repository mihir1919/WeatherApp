from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import LocSerializer
from .forms import LocationForm
from .models import Location
from django.http import JsonResponse
import requests,json

# Create your views here.

# class LocList(APIView):
#     def get(self):
        

#     def post(self):
#         pass


def index(request):
    return render(request,'track/index.html',{})
    


def res(request):
    l=['Adilabad', 'Agra', 'Ahmedabad', 'Ahmednagar', 'Aizawl', 'Ajitgarh(Mohali)', 'Ajmer', 'Akola', 'Alappuzha', 'Aligarh', 'Alirajpur', 'Allahabad', 'Almora', 'Alwar', 'Ambala', 'Ambedkar Nagar', 'Amravati', 'Amreli district', 'Amritsar', 'Anand', 'Anantapur', 'Anantnag', 'Angul', 'Anjaw', 'Anuppur', 'Araria', 'Ariyalur', 'Arwal', 'Ashok Nagar', 'Auraiya', 'Aurangabad', 'Aurangabad', 'Azamgarh', 'Badgam', 'Bagalkot', 'Bageshwar', 'Bagpat', 'Bahraich', 'Baksa', 'Balaghat', 'Balangir', 'Balasore', 'Ballia', 'Balrampur', 'Banaskantha', 'Banda', 'Bandipora', 'Bangalore Rural', 'Bangalore Urban', 'Banka', 'Bankura', 'Banswara', 'Barabanki', 'Baramulla', 'Baran', 'Bardhaman', 'Bareilly', 'Bargarh(Baragarh)', 'Barmer', 'Barnala', 'Barpeta', 'Barwani', 'Bastar', 'Basti', 'Bathinda', 'Beed', 'Begusarai', 'Belgaum', 'Bellary', 'Betul', 'Bhadrak', 'Bhagalpur', 'Bhandara', 'Bharatpur', 'Bharuch', 'Bhavnagar', 'Bhilwara', 'Bhind', 'Bhiwani', 'Bhojpur', 'Bhopal', 'Bidar', 'Bijapur', 'Bijapur', 'Bijnor', 'Bikaner', 'Bilaspur', 'Bilaspur', 'Birbhum', 'Bishnupur', 'Bokaro', 'Bongaigaon', 'Boudh(Bauda)', 'Budaun', 'Bulandshahr', 'Buldhana', 'Bundi', 'Burhanpur', 'Buxar', 'Cachar', 'Central Delhi', 'Chamarajnagar', 'Chamba', 'Chamoli', 'Champawat', 'Champhai', 'Chandauli', 'Chandel', 'Chandigarh', 'Chandrapur', 'Changlang', 'Chatra', 'Chennai', 'Chhatarpur', 'Chhatrapati Shahuji Maharaj Nagar', 'Chhindwara', 'Chikkaballapur', 'Chikkamagaluru', 'Chirang', 'Chitradurga', 'Chitrakoot', 'Chittoor', 'Chittorgarh', 'Churachandpur', 'Churu', 'Coimbatore', 'Cooch Behar', 'Cuddalore', 'Cuttack', 'Dadra and Nagar Haveli', 'Dahod', 'Dakshin Dinajpur', 'Dakshina Kannada', 'Daman', 'Damoh', 'Dantewada', 'Darbhanga', 'Darjeeling', 'Darrang', 'Datia', 'Dausa', 'Davanagere', 'Debagarh (Deogarh)', 'Dehradun', 'Deoghar', 'Deoria', 'Dewas', 'Dhalai', 'Dhamtari', 'Dhanbad', 'Dhar', 'Dharmapuri', 'Dharwad', 'Dhemaji', 'Dhenkanal', 'Dholpur', 'Dhubri', 'Dhule', 'Dibang Valley', 'Dibrugarh', 'Dima Hasao', 'Dimapur', 'Dindigul', 'Dindori', 'Diu', 'Doda', 'Dumka', 'Dungapur', 'Durg', 'East Champaran', 'East Delhi', 'East Garo Hills', 'East Khasi Hills', 'East Siang', 'East Sikkim', 'East Singhbhum', 'Eluru', 'Ernakulam', 'Erode', 'Etah', 'Etawah', 'Faizabad', 'Faridabad', 'Faridkot', 'Farrukhabad', 'Fatehabad', 'Fatehgarh Sahib', 'Fatehpur', 'Fazilka', 'Firozabad', 'Firozpur', 'Gadag', 'Gadchiroli', 'Gajapati', 'Ganderbal', 'Gandhinagar', 'Ganganagar', 'Ganjam', 'Garhwa', 'Gautam Buddh Nagar', 'Gaya', 'Ghaziabad', 'Ghazipur', 'Giridih', 'Goalpara', 'Godda', 'Golaghat', 'Gonda', 'Gondia', 'Gopalganj', 'Gorakhpur', 'Gulbarga', 'Gumla', 'Guna', 'Guntur', 'Gurdaspur', 'Gurgaon', 'Gwalior', 'Hailakandi', 'Hamirpur', 'Hamirpur', 'Hanumangarh', 'Harda', 'Hardoi', 'Haridwar', 'Hassan', 'Haveri district', 'Hazaribag', 'Hingoli', 'Hissar', 'Hooghly', 'Hoshangabad', 'Hoshiarpur', 'Howrah', 'Hyderabad', 'Hyderabad', 'Idukki', 'Imphal East', 'Imphal West', 'Indore', 'Jabalpur', 'Jagatsinghpur', 'Jaintia Hills', 'Jaipur', 'Jaisalmer', 'Jajpur', 'Jalandhar', 'Jalaun', 'Jalgaon', 'Jalna', 'Jalore', 'Jalpaiguri', 'Jammu', 'Jamnagar', 'Jamtara', 'Jamui', 'Janjgir-Champa', 'Jashpur', 'Jaunpur district', 'Jehanabad', 'Jhabua', 'Jhajjar', 'Jhalawar', 'Jhansi', 'Jharsuguda', 'Jhunjhunu', 'Jind', 'Jodhpur', 'Jorhat', 'Junagadh', 'Jyotiba Phule Nagar', 'Kabirdham (formerly Kawardha)', 'Kadapa', 'Kaimur', 'Kaithal', 'Kakinada', 'Kalahandi', 'Kamrup', 'Kamrup Metropolitan', 'Kanchipuram', 'Kandhamal', 'Kangra', 'Kanker', 'Kannauj', 'Kannur', 'Kanpur', 'Kanshi Ram Nagar', 'Kanyakumari', 'Kapurthala', 'Karaikal', 'Karauli', 'Karbi Anglong', 'Kargil', 'Karimganj', 'Karimnagar', 'Karnal', 'Karur', 'Kasaragod', 'Kathua', 'Katihar', 'Katni', 'Kaushambi', 'Kendrapara', 'Kendujhar (Keonjhar)', 'Khagaria', 'Khammam', 'Khandwa (East Nimar)', 'Khargone (West Nimar)', 'Kheda', 'Khordha', 'Khowai', 'Khunti', 'Kinnaur', 'Kishanganj', 'Kishtwar', 'Kodagu', 'Koderma', 'Kohima', 'Kokrajhar', 'Kolar', 'Kolasib', 'Kolhapur', 'Kolkata', 'Kollam', 'Koppal', 'Koraput', 'Korba', 'Koriya', 'Kota', 'Kottayam', 'Kozhikode', 'Krishna', 'Kulgam', 'Kullu', 'Kupwara', 'Kurnool', 'Kurukshetra', 'Kurung Kumey', 'Kushinagar', 'Kutch', 'Lahaul and Spiti', 'Lakhimpur', 'Lakhimpur Kheri', 'Lakhisarai', 'Lalitpur', 'Latehar', 'Latur', 'Lawngtlai', 'Leh', 'Lohardaga', 'Lohit', 'Lower Dibang Valley', 'Lower Subansiri', 'Lucknow', 'Ludhiana', 'Lunglei', 'Madhepura', 'Madhubani', 'Madurai', 'Mahamaya Nagar', 'Maharajganj', 'Mahasamund', 'Mahbubnagar', 'Mahe', 'Mahendragarh', 'Mahoba', 'Mainpuri', 'Malappuram', 'Maldah', 'Malkangiri', 'Mamit', 'Mandi', 'Mandla', 'Mandsaur', 'Mandya', 'Mansa', 'Marigaon', 'Mathura', 'Mau', 'Mayurbhanj', 'Medak', 'Meerut', 'Mehsana', 'Mewat', 'Mirzapur', 'Moga', 'Mokokchung', 'Mon', 'Moradabad', 'Morena', 'Mumbai City', 'Mumbai suburban', 'Munger', 'Murshidabad', 'Muzaffarnagar', 'Muzaffarpur', 'Mysore', 'Nabarangpur', 'Nadia', 'Nagaon', 'Nagapattinam', 'Nagaur', 'Nagpur', 'Nainital', 'Nalanda', 'Nalbari', 'Nalgonda', 'Namakkal', 'Nanded', 'Nandurbar', 'Narayanpur', 'Narmada', 'Narsinghpur', 'Nashik', 'Navsari', 'Nawada', 'Nawanshahr', 'Nayagarh', 'Neemuch', 'Nellore', 'New Delhi', 'Nilgiris', 'Nizamabad', 'North 24 Parganas', 'North Delhi', 'North East Delhi', 'North Goa', 'North Sikkim', 'North Tripura', 'North West Delhi', 'Nuapada', 'Ongole', 'Osmanabad', 'Pakur', 'Palakkad', 'Palamu', 'Pali', 'Palwal', 'Panchkula', 'Panchmahal', 'Panchsheel Nagar district (Hapur)', 'Panipat', 'Panna', 'Papum Pare', 'Parbhani', 'Paschim Medinipur', 'Patan', 'Pathanamthitta', 'Pathankot', 'Patiala', 'Patna', 'Pauri Garhwal', 'Perambalur', 'Phek', 'Pilibhit', 'Pithoragarh', 'Pondicherry', 'Poonch', 'Porbandar', 'Pratapgarh', 'Pratapgarh', 'Pudukkottai', 'Pulwama', 'Pune', 'Purba Medinipur', 'Puri', 'Purnia', 'Purulia', 'Raebareli', 'Raichur', 'Raigad', 'Raigarh', 'Raipur', 'Raisen', 'Rajauri', 'Rajgarh', 'Rajkot', 'Rajnandgaon', 'Rajsamand', 'Ramabai Nagar (Kanpur Dehat)', 'Ramanagara', 'Ramanathapuram', 'Ramban', 'Ramgarh', 'Rampur', 'Ranchi', 'Ratlam', 'Ratnagiri', 'Rayagada', 'Reasi', 'Rewa', 'Rewari', 'Ri Bhoi', 'Rohtak', 'Rohtas', 'Rudraprayag', 'Rupnagar', 'Sabarkantha', 'Sagar', 'Saharanpur', 'Saharsa', 'Sahibganj', 'Saiha', 'Salem', 'Samastipur', 'Samba', 'Sambalpur', 'Sangli', 'Sangrur', 'Sant Kabir Nagar', 'Sant Ravidas Nagar', 'Saran', 'Satara', 'Satna', 'Sawai Madhopur', 'Sehore', 'Senapati', 'Seoni', 'Seraikela Kharsawan', 'Serchhip', 'Shahdol', 'Shahjahanpur', 'Shajapur', 'Shamli', 'Sheikhpura', 'Sheohar', 'Sheopur', 'Shimla', 'Shimoga', 'Shivpuri', 'Shopian', 'Shravasti', 'Sibsagar', 'Siddharthnagar', 'Sidhi', 'Sikar', 'Simdega', 'Sindhudurg', 'Singrauli', 'Sirmaur', 'Sirohi', 'Sirsa', 'Sitamarhi', 'Sitapur', 'Sivaganga', 'Siwan', 'Solan', 'Solapur', 'Sonbhadra', 'Sonipat', 'Sonitpur', 'South 24 Parganas', 'South Delhi', 'South Garo Hills', 'South Goa', 'South Sikkim', 'South Tripura', 'South West Delhi', 'Sri Muktsar Sahib', 'Srikakulam', 'Srinagar', 'Subarnapur (Sonepur)', 'Sultanpur', 'Sundergarh', 'Supaul', 'Surat', 'Surendranagar', 'Surguja', 'Tamenglong', 'Tarn Taran', 'Tawang', 'Tehri Garhwal', 'Thane', 'Thanjavur', 'The Dangs', 'Theni', 'Thiruvananthapuram', 'Thoothukudi', 'Thoubal', 'Thrissur', 'Tikamgarh', 'Tinsukia', 'Tirap', 'Tiruchirappalli', 'Tirunelveli', 'Tirupur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Tonk', 'Tuensang', 'Tumkur', 'Udaipur', 'Udalguri', 'Udham Singh Nagar', 'Udhampur', 'Udupi', 'Ujjain', 'Ukhrul', 'Umaria', 'Una', 'Unnao', 'Upper Siang', 'Upper Subansiri', 'Uttar Dinajpur', 'Uttara Kannada', 'Uttarkashi', 'Vadodara', 'Vaishali', 'Valsad', 'Varanasi', 'Vellore', 'Vidisha', 'Viluppuram', 'Virudhunagar', 'Visakhapatnam', 'Vizianagaram', 'Vyara', 'Warangal', 'Wardha', 'Washim', 'Wayanad', 'West Champaran', 'West Delhi', 'West Garo Hills', 'West Kameng', 'West Khasi Hills', 'West Siang', 'West Sikkim', 'West Singhbhum', 'West Tripura', 'Wokha', 'Yadgir', 'Yamuna Nagar', 'Yanam', 'Yavatmal', 'Zunheboto']
    context={'l':l}
    return render(request,'track/res.html',context)

def resources(request,city):
    y=requests.get("https://api.covid19india.org/resources/resources.json")
    t2=(y.text)
    res2=json.loads(t2)
    l=[]
    for i in range(len(res2["resources"])):
        if(res2["resources"][i]["city"]==city):
            l.append((res2["resources"][i]))
            f=1
    s= 'track/resources.html'
    return render(request,s,{"l":l})
    # r=requests.get("https://api.covid19india.org/zones.json")
    # t=(r.text)
    # res=json.loads(t)
    # f=0
    # dis=""
    # state=""
    # zone=""
    # for i in range(732):
    #     if(res["zones"][i]["district"]==city):
    #         dis=(res["zones"][i]['district'])
    #         state=(res["zones"][i]['state'])
    #         zone=(res["zones"][i]["zone"])
    #         f=1
    #         break
    # if(f==0):
    #     for i in range(732):
    #         if("Delhi" in res["zones"][i]["district"]):
    #             print(res["zones"][i])
    # k=dis,state,zone
    # return HttpResponse(k)


def my_view(request,city):
    y=requests.get("https://api.covid19india.org/resources/resources.json")
    t2=(y.text)
    res2=json.loads(t2)
    data={}
    l=[]
    s=""
    for i in range(len(res2["resources"])):
        if(res2["resources"][i]["city"]==city):
            s=res2["resources"][i]["state"]
            l.append((res2["resources"][i]))
    data['resources']=l
    r=requests.get("https://api.covid19india.org/zones.json")
    t=(r.text)
    res=json.loads(t)
    f=0
    dis=""
    state=""
    zone=""
    nd=[]
    for i in range(732):
        if(res["zones"][i]["district"]==city):
            nd.append(res["zones"][i])
            f=1
            break
    if(f==0):
        for i in range(732):
            if(city in res["zones"][i]["district"]):
                nd.append(res["zones"][i])
    data['report']=nd
    return JsonResponse(data)

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