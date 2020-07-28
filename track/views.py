from django.shortcuts import render,redirect,HttpResponse
from .forms import LocationForm
from .models import Location
from django.http import JsonResponse
import requests,json
import tweepy
from geopy.geocoders import Nominatim
from textblob import TextBlob as T
from wordcloud import STOPWORDS,WordCloud
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


comment_words = ' '
stopwords = set(STOPWORDS)

def index(request):
    r=requests.get('http://newsapi.org/v2/top-headlines?country=in&apiKey=2d9ce72f1abe4c3bbbed367592c3ff44')
    t=(r.text)
    response=json.loads(t)
    l=[]
    if(response['status']=='ok'):
        for i in range(5):
            d={}
            d["source"]=response['articles'][i]['source']['name']
            d["author"]=response['articles'][i]['author']
            d["title"]=response['articles'][i]['title']
            d['img']=response['articles'][i]['urlToImage']
            d["desc"]=response['articles'][i]['description']
            l.append(d)
    return render(request,'track/index.html',{'l':l})

def news(request,topic):
    r=requests.get('http://newsapi.org/v2/top-headlines?country=in&category='+ str(topic) +'&apiKey=2d9ce72f1abe4c3bbbed367592c3ff44')
    t=(r.text)
    response=json.loads(t)
    l=[]
    if(topic):
        if(response['status']=='ok'):
            for i in range(5):
                d={}
                d["source"]=response['articles'][i]['source']['name']
                d["author"]=response['articles'][i]['author']
                d["title"]=response['articles'][i]['title']
                d['img']=response['articles'][i]['urlToImage']
                d["desc"]=response['articles'][i]['description']
                l.append(d)
    return render(request,'track/index.html',{'l':l})

def sitemap(request):
    return render(request,"track/sitemap.xml")


def res(request):
    l={'Andaman & Nicobar': {'Port Blair'}, 'Andhra Pradesh': {'Kakinada', 'Visakhapatnam', 'Kadapa', 'Tirupati', 'Kurnool', 'Vijayawada'}, 'Assam': {'Sivasagar', 'Sadiya', 'Nagaon', 'Guwahati City', 'Majuli', 'Kamrup', 'Bongaigaon', 'Karbi Anglong', 'Barpeta', 'Biswanath', 'Hojai', 'Udalguri', 'Tezpur', 'Morigaon', 'Sonitpur', 'Baksa', 'Hailakandi', 'Dima Hasao', 'Nalbari', 'Dhubri', 'Guwahati', 'Dibrugarh', 'Hamren', 'Jorhat', 'Lakhimpur', 'Silchar', 'Golaghat', 'South Salmara', 'Kokrajhar', 'Goalpara', 'Charaideo', 'Darrang', 'Karimganj', 'Chirang', 'Cachar', 'Dhemaji', 'Tinsukia', 'PAN State'}, 'Bihar': {'Muzzafarpur', 'Patna', 'Bihar Sharif', 'Darbhanga', 'Jehanabad', 'PAN State'}, 'Chandigarh': {'Chandigarh'}, 'Chhattisgarh': {'Bastar', 'Raigarh', 'Katghora', 'Mahasamund', 'Janjgir', 'Korba', 'Surajpur', 'Bilaspur', 'Jagdalpur', 'Dhamtari', 'Raipur', 'Balod', 'Mungeli', 'jashpur nagar', 'Kabirdham', 'Sukma', 'Bemetara', 'Rajnandgaon', 'Korea', 'Naraynpur', 'Dantewada', 'Balrampur', 'Baloda Bazar', 'PAN State'}, 'Delhi': {'New Delhi', 'Delhi'}, 'Goa': {'Panaji', 'Bambolim'}, 'Gujarat': {'Rajkot', 'Vadodara', 'Morbi', 'Surat', 'Bhavnagar', 'Ahmedabad', 'Jamnagar'}, 'Haryana': {'Gurgaon', 'Sonepat', 'Rohtak', 'Faridabad'}, 'Himachal Pradesh': {'Kangra', 'Shimla'}, 'Jammu & Kashmir': {'Udhampur', 'Srinagar', 'Jammu'}, 'Jharkhand': {'Dhanbad', 'Sahibganj', 'Ranchi', 'Jamshedpur', 'Khunti', 'Pakur', 'Hamirpur', 'Deoghar', 'Bokaro', 'Hazaribagh', 'PAN State', 'West Singhbhum'}, 'Karnataka': {'Tumkur', 'Shimoga', 'Bangalore', 'Bellary', 'Belgaum', 'Udupi', 'Gulbarga', 'Mysore', 'Hassan', 'Mangalore', 'Bidar', 'Hubli–Dharwad'}, 'Kerala': {'Kodakara', 'Thanniam', 'Clappana', 'Kottnadu', 'Manjapra', 'Tuneri', 'Kulasekharapuram', 'Kadangod', 'Wayanad', 'Edavaka', 'Mankulam', 'Kozhencherry', 'Mullenkolly', 'Alankode', 'Nadathara', 'Othukungal', 'Uzhavoor', 'Puramattom', 'Thiruvali', 'Haripad', 'Mokeri', 'Paatyam', 'Kanjiramkulam', 'Paippadu', 'Mala', 'Akathethara', 'Cherpu', 'Ayyankunnu', 'Kadakkavoor', 'Iritty', 'Koduvally', 'Thidanadu', 'Niranam', 'Keerampara', 'Karoor', 'Chapparapadavu', 'Koodaranhi', 'Kottayi', 'Malappuram', 'Kannadi', 'Mukkam', 'Puthenchira', 'Kattakambal', 'Nedumpana', 'Varavoor', 'Marangattupally', 'Cheranalloor', 'Cherupuzha', 'Cheruvannur', 'Kanichar', 'Kumarampathur', 'Kalloorkkad', 'Mayyanad', 'Manarkadu', 'Melattur', 'Kadambazhippuram', 'Mundakkayam', 'Vanimel', 'Alagappanagar', 'Chennithala', 'Pattithara', 'Angamaly', 'Azhiyur', 'Pothencode', 'Ramanattukara', 'Anchal', 'Sholayur', 'Thrikkunnapuzha', 'Elakamon', 'Seethathode', 'Thaliparamba', 'Nedumkandom', 'S N Puram', 'Kaniyambetta', 'Mepayyur', 'Nedumbassery', 'Nenmanikkara', 'Naranganam', 'Chittur ULB', 'Kochi', 'Keezhariyur', 'Koyilandy', 'Kizhakoth', 'Mananthavady', 'Thriunavaya', 'Keezhallur', 'Chokli', 'Panachikadu', 'Pattambi', 'Panayam', 'Chittar', 'Melila', 'Manjeri', 'Pramadam', 'Venkitangu', 'Pannyannur', 'Kottoppadam', 'Muhamma', 'Kodumon', 'Keezhuparamba', 'Thrikkovilvattom', 'Devikulam', 'Moonnilavu', 'Kadakkal', 'Thirumittakode', 'Thuvvur', 'Aloor', 'Nadapuram', 'Veeyapuram', 'Mudakkal', 'Alappad', 'Nedumpram', 'Vakathanam', 'Changanacherry', 'Kannur', 'Punnayoorkulam', 'Kavasserri', 'Marutharoad', 'Mulakulam', 'Kannamangalam', 'Vengara', 'Ayancheri', 'Kanjoor', 'Paingottoor', 'Parli', 'Punalur', 'Mannur', 'Kunnathunad', 'Chemmaruthi', 'Maloor', 'Poothakkulam', 'Tirurangadi', 'Vellanad', 'Chenkal', 'Chingoli', 'Vellavoor', 'Kulanada', 'Ramamangalam', 'Vadanappilly', 'Mattanur', 'Amboori', 'Irimbiliyam', 'Kallikkadu', 'Nelliampathy', 'Rayamangalam', 'Eraviperoor', 'Amarambalam', 'Koovappady', 'Neendoor', 'Nilambur', 'Ottasekharamangalam', 'Ponnani', 'Eloor', 'Ala', 'Naduvannur', 'Thakazhi', 'Kothamangalam', 'Kooroppada', 'Irikkur', 'Ayarkunnam', 'Vazhikkadavu', 'Pattazhi', 'Oorakam', 'Vannapuram', 'Chelembra', 'Chembilode', 'Kulathoor', 'Arikkulam', 'Feroke', 'Veliyannoor', 'Anthikkad', 'Perumanna Klari', 'Pulamanthole', 'Vazhoor', 'Moothedam', 'Payyanur', 'Navaikulam', 'Chakkittappara', 'Nemmara', 'Chettikulangara', 'Munnar', 'Chinnakanal', 'Varkkala', 'Kannambra', 'Moodady', 'Pazhayannur', 'Malayattoor', 'Payyavoor', 'Chengottukavu', 'Edarikode', 'Kavanur', 'Trithala', 'Vettom', 'Vadakkekkara', 'M G Kavu', 'Thiruvambady', 'Thalayolaparambu', 'Kadaplamattom', 'Elamkulam', 'Peralassery', 'Vilappil', 'Kalpakanchery', 'Bathery', 'Eruvessi', 'Kollam East', 'Vechoochira', 'Pallickal', 'Aruvappulam', 'Kappur', 'Pariyaram', 'Pandalam Municipality', 'Thalayazham', 'Koothali', 'Kaduthuruthy', 'Thekkumkara', 'Thanalur', 'Oachira', 'Kunnamthanam', 'Omallor', 'Madayi', 'Karthikapally', 'Mulavukad', 'Thekkumbhagom', 'Cheruthana', 'Uzhamalaykkal', 'Manimala', 'Marakkara', 'Kasaragod', 'THRIPUNITHURA', 'Vadakkekkad', 'Sooranadu South', 'Vettor', 'Vilakkudy', 'Mathur', 'Neendakara', 'Kottuvally', 'Muriyad', 'Elavanchery', 'Ambalavayal', 'Karunapuram', 'Kummil', 'Pallippad', 'Pappinisseri', 'Thenkkurrussi', 'Vattamkulam', 'Pattuvam', 'Kanakkary', 'Nannambra', 'Sreekandapuram', 'Balussery', 'Polpully', 'Kadannapalli', 'Aryad', 'Thachampara', 'Valayam', 'Kalloopara', 'Thondernadu', 'Malayalppuzha', 'Olavanna', 'Kottiyoor', 'Cheppad', 'Kayakkodi', 'Madavoor', 'Mankada', 'shoranur', 'Pananchery', 'Alapadambu', 'Azhoor', 'Vazhakulam', 'Padiyoor', 'Arakulam', 'Makkaraparamu', 'Perinad', 'Rajakkadu', 'Thenmala', 'Ambalappuzha', 'Punnayoor', 'Kulathupuzha', 'Thalavady', 'Chavara', 'Unnnikulam', 'Kottarakkara', 'Choornikkara', 'Engandiyoor', 'Piravanthoor', 'Thodupuzha municipality', 'Kottakkal', 'Elamkunnapuzh.', 'Kumbalam', 'Kadamakkudy', 'Kudayathoor', 'Veloor', 'Karode', 'Koothattukulam', 'Mundoor', 'Bysonvalley', 'Chellanam', 'Vellinezhi', 'Perumatti', 'Neduvathoor', 'Puthuppadi', 'Agali', 'Kumaly', 'Bharanikkavu', 'Vadakara', 'Njarakka', 'Pothanikkad', 'Mulakkuzha', 'Thiruvallur', 'Udhayamperoor', 'Kaippamangalam', 'Paruthur', 'Puzhakkattiri', 'Chengamanade', 'Chirakkadavu', 'Purappuzha', 'Karinkunnam', 'Nedumkunnam', 'Perambra', 'Elamadu', 'MUZHAKKUNNU', 'Puthupariyaram', 'Orumanyoor', 'Pudukkad', 'Nannamukku', 'Edachery', 'Vandazhi', 'Poomangalam', 'Alathur', 'Kongad', 'Maranchery', 'Mundrothuruthu', 'Villyappalli', 'Attingal', 'Elavally', 'Nanminda', 'Thalakkulathur', 'Mallappuzhassery', 'Desamangalam', 'Thrikkakara West', 'Mangalam', 'Vadavukode Puthancruz', 'Okkal', 'Vazhayur', 'Venmony', 'Erattupetta', 'Purameri', 'Thottappuzhassery', 'Meppadi', 'Thollur', 'Thrikkalangode', 'Pallipuram', 'Chathannur', 'Moorkanad', 'Thalakkad', 'Palakkad ulb', 'Thrikkaruva', 'Pattencherry', 'Kangazha', 'Aymanam', 'Bharananganam', 'Changaroth', 'Madappally', 'Erimayur', 'Vallapuzha', 'Matool', 'Valakom', 'Thurayur', 'Koyipuram', 'Thannithode', 'Anthoor', 'Perayam', 'Maniyur', 'Thalavoor', 'Pozhuthana', 'Kanjirappuzha', 'Koottilangadi', 'Kunjimanagalam', 'Kunnathukal', 'Njeezhoor', 'Kumbalangy', 'Alappuzha', 'Maangattidam', 'Kumarakom', 'Kottangal', 'Puthukodu', 'Thikkodi', 'Udayanapuram', 'Moopainad', 'Thrikkodithanam', 'Velookkara', 'Ottappalam', 'Kaiparambu', 'Edapatta', 'Thiruvalla West', 'Varantharappilly', 'Aryankavu', 'Edappal', 'Kalliassery', 'Pirayiri', 'Chirakkara', 'Vallickode', 'Mararikulam', 'Valapattanam', 'Panoor', 'Neyyattinkara Cds', 'Kolachery', 'Mynagappally', 'Valappad', 'Kannapuram', 'Thamarassery', 'Edavetty', 'Kadanadu', 'Mezhuveli', 'Muttom', 'Eroor', 'Vazhathope', 'Karumalloor', 'Champakulam', 'Pooyappally', 'Elanji', 'Thiruvilwamala', 'Chemencherry', 'Chirayinkeezhu', 'Edathala', 'Padinjarathra', 'Pallarimangalam', 'Kainakary', 'Narikunni', 'Aralam', 'Peringom Vayakkara', 'Marayoor', 'Perumpadappu', 'Vallachira', 'Kulukkallur', 'Thiruvaniyoor', 'Adat', 'Kuthiyathode', 'Velloor', 'Naranammoozhi', 'Karuvatta', 'Poothadi', 'Ranni Angadi', 'Ittiva', 'Kathirur', 'Kumaramangalam', 'Mavoor', 'Thekkekkara', 'Parassala', 'Chennerkara', 'Thenhipalam', 'Pavaratty', 'Cherukavu', 'Kanjikuzhi', 'Mannarkkad', 'Kizhuvilam', 'Alackode', 'Nanniyode', 'Edayur', 'Sasthamcotta', 'Ambalappara', 'Eranjoli', 'Kadapra', 'kalpetta', 'Muzhappilangad', 'Vaniyamkulam', 'Vengad', 'Nooranad', 'Panangad', 'Mararikkulam', 'Manjoor', 'Pandalam Thekkekara', 'Thillenkeri', 'Vazhappally', 'Pattazhi North', 'Thumpamon', 'Kuttiyatoor', 'New mahi', 'Theekoy', 'Avanoor', 'Kondotty', 'panamaram', 'Ezhumattoor', 'Pookkottukavu', 'Tanur', 'Thiruvarppu', 'Vijayapuram', 'Oorngattiri', 'Kokkyar', 'puliyoor', 'purakkad', 'Elikulam', 'Edavanna', 'Karassery', 'Kumarapuram', 'Vallikunnam', 'Vellathooval', 'Kelakam', 'Aranmula', 'Purathur', 'Elapully', 'Cherukunnu', 'Chengannur', 'Santhenpara', 'Maravanthuruthu', 'Ayyampuzha', 'Kodur', 'Pootrikka', 'Karunagappally', 'Krishnapuram', 'Mookkannoor', 'Pallassana', 'Edamulakkal', 'Cheriyamundam', 'Nattika', 'Ambalppuzha', 'Mannar', 'Perumbavoor', 'Vakkom', 'Karalam', 'Kalamassery', 'Maradu', 'Adoor', 'Velliyamattam', 'Tirur', 'Varapuzha', 'Parathodu', 'Cheekode', 'Poonjar', 'Cherunniyoor', 'Niramaruthur', 'Peruvayal', 'Pothukal', 'Kollemkode', 'Chadayamangalam', 'Thenkara', 'Kuttampuzha', 'Payyoli', 'Aroor', 'West Kallada', 'kunnathunadu', 'Ponmala', 'Kunnothuparambu', 'Alangad', 'Thiruvalla East', 'Ramankary', 'Thiruvankulam', 'Vengoor', 'Rajakumari', 'Thrikkadeeri', 'T.V. Puram', 'Ezhukone', 'Vandiperiyar', 'Omasseri', 'Panjal', 'Sreekrishnapuram', 'Kalikavu', 'Parappur', 'Chaliyar', 'Meenachil', 'Annamanada', 'Malampuzha', 'Mangalapuram', 'Kunnukara', 'Wandoor', 'Thodiyoor', 'Amballoor', 'Kolayad', 'Ulliyeri', 'Devikulangara', 'Narath', 'Konni', 'Pulpatta', 'Koothuparamba', 'Kayamkulam', 'Cherppalasseri', 'Mullassery', 'Kottamkara', 'Nenmeni', 'Kurichy', 'Pathanamthitta', 'Elampalloor', 'Kallara', 'Assamannoor', 'Thevalakkara', 'Karimannoor', 'Muthuthala', 'Thazhakkara', 'Aluva', 'Vechoor', 'Karumkulam', 'Vellarada', 'Andoorkonam', 'PERAVOOR', 'Chowannur', 'Azhikode', 'Kadampanad', 'Vadavannur', 'Kollam', 'Meenadam', 'Kavalam', 'Kakkur', 'Kodumbu', 'Vettathur', 'Palamel', 'Ummannur', 'Punnappara North', 'A.R. Nagar', 'Kollayil', 'Aliparamba', 'Thalanadu', 'Parappananagadi', 'Chennam Pallippuram', 'Moopainadu', 'Ezhome', 'Eramala', 'Kuzhimanna', 'Peruvallur', 'pulpally', 'Vallatholenagar', 'Erumely', 'Kavalangad', 'Vettikkavala', 'Lekkidi Peroor', 'Padyoor', 'Vadasserikara', 'Kuruvattoor', 'Keezhmad', 'Kodamthuruth', 'Udayagiri', 'irinjalakuda block panchayath', 'Poruvazhy', 'Kondazhy', 'Mylapara', 'Peruvemba', 'Mananthavadi', 'Ongallur', 'kothamangalam', 'Peermade', 'Parakkadavu', 'Thiruvananthapuram', 'Vayalar', 'Guruvayur', 'Koorachundu', 'Puthur', 'Velinallur', 'Veliyanad', 'Edakkara', 'Venganoor', 'Manakkadu', 'Nedumudy', 'Sholaur', 'Keralasseri', 'Thamarakkulam', 'Kuthanur', 'Kattappana Municipality', 'Karulai', 'Ezhamkulam', 'Kattippara', 'Pulincunnu', 'Ulikkal', 'Manaloor', 'Pallikkal', 'Thirupuram', 'Pampakkuda', 'Poovar', 'Panavally - ruchi', 'Vandanmedu', 'Chittattukara', 'Erath', 'Alanallur', 'Tharur', 'Munniyur', 'Enadimangalam', 'Perumkadavila', 'Vathikudy', 'Mankara', 'Kalanjoor', 'Kavilumpara', 'Nilamel', 'Kunnummel', 'Nochad', 'Peringara', 'Thuravur', 'Vythiri', 'Vadakarapathy', 'Karimpuzha', 'Kottur', 'Kadavallur', 'Thirunelly', 'Thiruvegappura', 'Vilayur', 'Pulimath', 'Parapookkara', 'Chengalai', 'Kuttippuram', 'payam', 'Cheruthazham', 'Kuzhalmannam', 'nallepilly', 'Mattathoor', 'Tavanur', 'Manamboor', 'Ozhur', 'Anjarakandi', 'Kodassery', 'PAN State', 'Chunakkara', 'Cherukol', 'Chithara', 'Kurumathoor', 'Adichanallur', 'Triprangottur', 'Valavannur', 'Aikkaranad', 'Chakkupallam', 'Chirakkal', 'Morayur', 'Mayyil', 'Perumanna', 'Kunnamangalam', 'Pampady', 'Mariyapuram', 'Ayyappancovil', 'Anikad', 'Karavaram', 'Muttil', 'Paipra', 'Maruthonkara', 'Mullurkkara', 'Pazhayakunnumel', 'Thalassery', 'Koratty', 'Kakkodi', 'Kalpetta', 'Pinarayi', 'Sreemoola nagaram', 'Upputhara', 'Thazhava', 'Perinjanam', 'Chokkad', 'Kozhuvanal', 'Kunnathoor', 'Chavakkad', 'Vellangallur', 'Vithura', 'Edathua', 'Meenanagadi', 'Konnathadi', 'Ramanthalli', 'Thalappalam', 'Atholi', 'Muthuvallur', 'Malayinkeezhu', 'Pathiyoor', 'Wadakkanchery', 'Kundara', 'Ranni Pazhavangadi', 'Mudakkuzha', 'Maneed', 'Mallappally', 'Kuruva', 'Chittariparamb', 'Nayarambalam', 'Kottayam', 'Thazhekode', 'Vengola', 'Karimba', 'Karuvarakund', 'Veliyam', 'Akalakunnam', 'Thrikkakara East', 'Karukachal', 'Mathilakam', 'Vadakkenchery', 'Areacode', 'Puthunagaram', 'Edavanakkad', 'Dharmadam', 'Kodenchery', 'Panmana', 'Irinjalakkuda', 'Chendamangalam', 'Anakkayam', 'Meloor', 'Kunnamkulam', 'Thirumarady', 'Karakurissi', 'Onchium', 'Thrikoor', 'Puthanvelikkara', 'Chorode', 'Arpookkara', 'Chazhoor', 'Kanchiyar', 'Kadukutty', 'Eruthenpathy', 'Kuttichal', 'Sooranadu North', 'Muttar', 'Kizhekkencheri', 'Budhanoor', 'Neelamperoor', 'chalavara', 'Ananganadi', 'Kattoor', 'Pindimana', 'Chalakudy', 'Ponmudam', 'Naripetta', 'Angadippuram', 'Kaladi', 'Thachanattukara', 'Noolpuzha', 'Thycattussery', 'Kozhikode', 'Avoly', 'Ramapuram', 'Piravam', 'Vaikom', 'Valanchery', 'Punnapra South', 'Perinthalmanna', 'Chathamangalam', 'Keezhattur', 'Vellamunda', 'pandanad', 'Aryankode', 'Chelannur', 'Koruthodu', 'Koduvayur', 'Porur', 'Kadambur', 'Chekkyad', 'Nagalasserri', 'Vazhakkad', 'pariyaram', 'Kandanassery', 'Mannnchery', 'Thanneermukkom', 'Chalisserri', 'Puthupally', 'Pattanakkad', 'Eramam', 'Melarkodu', 'Kayanna', 'Cheriyanad', 'Naduvil', 'Perunad', 'Kareepra', 'Arakuzha', 'Eriyad', 'Manickal', 'Pala', 'Kadamakudy', 'Kandalloor', 'Elappara', 'Kaviyoor', 'Muthalamada', 'Kanjirappally', 'Peringottukkurrissi', 'Edakkattuvayal', 'Kadakkarapally', 'Thavinjal', 'Munderi', 'Kozhinjampara', 'Vattavada', 'Athiyannoor', 'Pandikkad', 'Mylom', 'Ettumanoor', 'Pallivasal', 'Ezhupunna', 'Pavithreswaram', 'Kulakkada', 'Paravoor', 'Adimali', 'Thrissur', 'Alakkode', 'Puthusseri', 'Thuravoor', 'Shoranur', 'Nellaya', 'Kottathara', 'Ranni', 'Pookkottur', 'Mannacherry', 'Kalady', 'Karavaloor', 'Arookutty', 'Mavelikkara ULB', 'Senapathy', 'Manjallur', 'Athirampuzha', 'Ayavana', 'Kodungallur', 'Kizhakkekallada', 'Elanthoor', 'Kadalundi', 'Koppam', 'Velom', 'Kadinamkulam', 'Kanthaloor', 'Alayamon', 'Cherthala', 'Vengapally', 'Kuttor', 'Mampad', 'Kuttyadi', 'Karivellur Peralam', 'Ayroor', 'Veliyamcode', 'Malapattam', 'Ayilur', 'Ezhikkara', 'Kottukal', 'Kuravilangadu', 'Pulikkal', 'Anakkara', 'Koottickal', 'Edathiruthi', 'Porkulam', 'Choondal', 'Thariode', 'ottapalam', 'Vallikunnu', 'Athavanad', 'Perumbalam', 'thiruvanvandoor', 'Kalluvathukkal', 'Arattupuzha', 'Edavilangu', 'Thriprangode', 'Kidangoor', 'Mulanthuruthy', 'Poonjar Thekkekkara', 'Pallickathodu', 'Chungathara', 'Pathanapuram', 'Melukavu', 'Kuzhuppily'}, 'Madhya Pradesh': {'Datia', 'Bhind', 'Betul', 'Neemuch', 'Sehore', 'Shahdol', 'Sagar', 'Hoshangabad', 'Harda', 'Jhabua', 'Dindori', 'Narsinghpur', 'Shivpuri', 'Guna', 'Mandsaur', 'Panna', 'Tikamgarh', 'Singrauli', 'Shajapur', 'Indore', 'Gwalior', 'Katni', 'Barwani', 'Dewas', 'Bhopal', 'Mandla', 'Sheopur', 'Burhanpur', 'Jabalpur', 'Balaghat', 'Rewa', 'Morena', 'Chhindwara', 'Rajgarh', 'Anuppur', 'Vidisha', 'Satna', 'Raisen', 'Seoni', 'Sidhi', 'Ujjain', 'Agar Malwa', 'Khargone', 'Ratlam', 'Umaria', 'Chhatarpur', 'Khandwa', 'Dhar', 'Alirajpur', 'Niwari', 'Ashok Nagar', 'Damoh'}, 'Maharashtra': {'Pune', 'Parbhani', 'Amravati', 'Pimpri Chinchwad', 'Jalna', 'Solapur', 'Miraj', 'Aurangabad', 'Mumbai', 'Nagpur', 'Nasik City', 'Dhule', 'Nandurbar', 'Thane', 'Wardha', 'Mira Road', 'Udgir', 'Kalyan-Dombivli', 'Navi Mumbai', 'Palghar', 'Sangli', 'Akola', 'Bhayander', 'Latur', 'Nashik', 'Ahmednagar', 'PAN State'}, 'Manipur': {'Imphal'}, 'Meghalaya': {'', 'East Garo Hills', 'Khliehriat', 'South West Garo Hills', 'Tura', 'North Garo Hills', 'Jowai', 'West Garo Hills', 'Mairang', 'Williamnagar', 'South Garo Hills', 'East Jaintia Hills', 'Mariang', 'Dhankheti', 'Nongstoin', 'Baghmara', 'Shillong', 'Mawkyrwat', 'Ampati', 'Nongpoh'}, 'Odisha': {'Cuttack', 'Bhubaneswar', 'Boudh'}, 'PAN India': {'PAN State'}, 'Puducherry': {'Puducherry'}, 'Punjab': {'Majitha', 'Pathankot', 'Baba Bakala', 'Rajasansi', 'Patiala', 'Chheharta', 'New Amritsar', 'Ajnala', 'Amritsar', 'Kharar', 'Ludhiana', 'Goniana', 'Lopoke', 'Faridkot', 'Manawala', 'Jandiala Guru', 'Hoshiarpur', 'Rayya', 'Verka', 'Mohali (SAS Nagar)', 'Chogawan'}, 'Rajasthan': {'Dholpur', 'Jhalawar', 'Jhunjhunu', 'Tonk', 'Udaipur', 'Sri Ganganagar', 'Jaipur Rural', 'Kota City', 'Ajmer', 'Kota Rural', 'Dungarpur', 'Barmer', 'Dausa', 'Chittorgarh', 'Jodhpur Rural', 'Nathdwara', 'Grp Ajmer', 'Sirohi', 'Sawai Madhopur', 'Bikaner', 'Bharatpur', 'Banswara', 'Pratapgarh', 'Jhunjhunuu', 'Pali', 'Sriganganagar', 'Kota', 'Bundi', 'Jalore', 'Karauli', 'Jodhpur', 'Rajsamand', 'Hanumangarh', 'Bhilwara', 'Sikar', 'Jaipur', 'Alwar', 'Ganganagar', 'Baran', 'Jaisalmer', 'Churu', 'Nagaur', 'PAN State', 'Grp Jodhpur'}, 'Tamil Nadu': {'Tenkasi', 'Sivaganga', 'Cuddalore', 'Dharmapuri', 'Virudhunagar', 'Chennai', 'Chengalpattu', 'Theni', 'Ariyalur', 'Thoothukudi', 'Villupuram', 'Dindugul', 'Thanjavur', 'Vellore', 'Krishnagiri', 'Kanyakumari', 'Trichy', 'Tiruvannamalai', 'Madurai', 'Tiruvallur', 'Tiruvarur', 'Tirunelveli', 'Pudukottai', 'Ramanathapuram', 'Ranipet', 'Tiruchirappalli', 'Karur', 'Coimbatore', 'Tiruppur', 'Nagercoil', 'Salem', 'The Nilgiris', 'Thiruvarur', 'Tirupattur', 'Kallakurichi', 'Kancheepuram', 'Perambalur', 'Erode', 'Namakkal', 'Nagapattinam'}, 'Telangana': {'Jagtial', 'Asifabad', 'Yadadri Bhongiri', 'Medak', 'Kamareddy', 'Rajanna Siricilla', 'Cyberabad', 'Warangal Urban', 'Kumuram Bheem Asifabad', 'Hyderabad', 'Warangal', 'Secunderabad', 'Janagoan', 'Sangareddy', 'Vikarabad', 'Mahbubnagar', 'Bhupalpally', 'Khammam', 'Mahabubnagar', 'Nirmal', 'Nizamabad', 'Nalgonda', 'Jangaon', 'Bhadradri Kothagudem', 'Warangal Rural', 'Karimnagar', 'Wanaparthy', 'Ranga reddy', 'Narayanpet', 'Medchal Malkajgiri', 'Ranga Reddy', 'Mulugu', 'Rangareddy', 'Kothagudem', 'Peddapally', 'Gadwal', 'Suryapet', 'Warangal Urban & Rural', 'Yadadri Bhuvanagiri', 'Rajanna Sircilla', 'Mancherial', 'Peddapalli', 'Siddipet', 'Jogulamba Gadwal', 'Nagarkurnool', 'Jayashankar Bhupalapally', 'Adilabad', 'Mahabubabad', 'Medchal', 'PAN State'}, 'Uttar Pradesh': {'Baghpat', 'Bulandshahar', 'Noida', 'Ghaziabad', 'Gorakhpur', 'Saifai', 'Lucknow', 'Aligarh', 'Meerut', 'Allahabad', 'Varanasi', 'Agra', 'PAN State'}, 'West Bengal': {'Alipurduar', 'Kolkata', 'Midnapore', 'Berhampore', 'Howrah', 'Siliguri'}, 'Sikkim': {'Gangtok'}, 'Tripura': {'Agartala'}, 'Uttarakhand': {'Rishikesh', 'Haldwani', 'Dehradun'}}
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


    
def dis_view(request,state):
    y=requests.get("https://api.covid19india.org/state_district_wise.json")
    t2=y.text
    res2=json.loads(t2)
    data={}
    l=[]
    s=""
    l.append(res2[state])
    data[state]=l
    return JsonResponse(data)

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
            url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2edc88045665cd7d7e9ce52053e0948a'
            city=(request.POST.get("Country"))
            r = requests.get(url.format(city)).json()
            w_da={}
            if len(r) == 2:
                if r['message']=='city not found':
                    return HttpResponse("Not Found")
            w_da = {
                'city' : city,
                'temperature' : r['main']['temp'],
                'icon' : r['weather'][0]['icon'],
                'description' : r['weather'][0]['description']
            }
            print(w_da)   
            al = []
            for i in n:
                if str(i.Country) == str(city):
                    rr=False
            if rr==True:
                form.save()
                n=Location.objects.all()
            for i in n:
                r = requests.get(url.format(i.Country)).json()
                #print(r)
                w_d = {
                    'city' : i.Country,
                    'temperature' : r['main']['temp'],
                    'icon' : r['weather'][0]['icon'],
                    'description' : r['weather'][0]['description']
                }
                al.append(w_d)
            #print (al)
            #print(r)
            form = w_d
            return render(request,'track/result.html',{'al':al,'w_da':w_da})
    else:
        form = LocationForm()
    return render(request, 'track/tracker.html', {'form': form})

def twitter(request):
    CONSUMER_KEY = 'vG4qN6vZn47PfLvQiOl5vEgwI'
    CONSUMER_SECRET = 'I50fXTBjtopq2jAkfztGwFmifOLpYj0tshRSyruOThFRgNnMr8'
    ACCESS_KEY = '3141790171-XjYckAXh1NrgTUgJvZ4y5JCOiDmcAps2YyByP2z'
    ACCESS_SECRET = '4dbPGQK0voro1tRhMwcGnw1wjdCjLPxpNnAQIbBQInioc'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    search_words = "#COVID19India"
    n=20
    country="India"
    district="Hauz Khas"
    city="New Delhi"
    rangee=30
    if (request.method == "POST"):
        search_words = request.POST.get("topic")
        n=int(request.POST.get("no"))
        city = request.POST.get("city")
        country = request.POST.get("country")
        district = request.POST.get("district")
        rangee=int(request.POST.get("rangee"))
    api = tweepy.API(auth)
    locator = Nominatim(user_agent="track")
    location = locator.geocode(str(country))
    print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
    Latitude = location.latitude
    Longitude = location.longitude
    print(str(Latitude)+','+str(Longitude)+',1km')
    tweets = tweepy.Cursor(api.search,q=search_words,geocode=str(Latitude)+','+str(Longitude)+','+str(rangee)+'km',lang="en").items(n)
    d={}
    i=1
    labels=["Positive","Neutral","Negative"]
    data=[0.0,0.0,0.0]
    stri=""
    for tweet in tweets:
        #print(tweet.text)
        stri+=tweet.text
        f=T(tweet.text)
        ff=(list(f.sentiment))
        ff[0]=round(ff[0],3)
        ff[1]=round(ff[1],3)
        if(ff[0]<0.00):
            data[2]+=1
        elif(ff[0]==0.00):
            data[1]+=1
        elif(ff[0]>0.00):
            data[0]+=1
        l=[tweet.text,ff]
        d[i]=l
        i+=1
    # word_cloud  = WordCloud(width=800,height=800,background_color='white',stopwords=stopwords,min_font_size=10).generate(stri)
    # word_cloud.to_file(BASE_DIR+'track/static/images/Timage.png')
    t=i-1
    print(data)
    print(labels)
    return render(request,'track/twitter.html',{'d':d,'s':search_words,'t':t,'labels': labels,
        'data': data})

def normtwitter(request):
    CONSUMER_KEY = 'vG4qN6vZn47PfLvQiOl5vEgwI'
    CONSUMER_SECRET = 'I50fXTBjtopq2jAkfztGwFmifOLpYj0tshRSyruOThFRgNnMr8'
    ACCESS_KEY = '3141790171-XjYckAXh1NrgTUgJvZ4y5JCOiDmcAps2YyByP2z'
    ACCESS_SECRET = '4dbPGQK0voro1tRhMwcGnw1wjdCjLPxpNnAQIbBQInioc'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    d={}
    i=1
    labels=["Positive","Neutral","Negative"]
    data=[0.0,0.0,0.0]
    stri=""
    if (request.method == "POST"):
        tweets=api.search(request.POST.get('topic'))
        for tweet in tweets:
            #print(tweet.text)
            f=T(tweet.text)
            stri+=tweet.text
            ff=(list(f.sentiment))
            ff[0]=round(ff[0],3)
            ff[1]=round(ff[1],3)
            if(ff[0]<0.00):
                data[2]+=1
            elif(ff[0]==0.00):
                data[1]+=1
            elif(ff[0]>0.00):
                data[0]+=1
            l=[tweet.text,ff]
            d[i]=l
            i+=1
    # word_cloud  = WordCloud(width=800,height=800,background_color='white',stopwords=stopwords,min_font_size=10).generate(stri)
    # word_cloud.to_file('track/static/images/Timage.png')
    t=i-1
    return render(request,'track/nt.html',{'d':d,'s':request.POST.get('topic'),'t':t,'labels': labels,
        'data': data})

def snt(request):
    return render(request,'track/ntwitter.html')

def searchtwitter(request):
    return render(request, 'track/twit.html')
