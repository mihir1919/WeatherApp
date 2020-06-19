from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('<str:topic>/',views.news,name="news"),
    path('tracker/',views.tracker,name="tracker"),
    path('tes/',views.tes,name="tes"),
    path('res/',views.res,name="res"),
    path('res/<str:city>/', views.resources,name="resources"),
    path('yo/<str:city>/',views.my_view,name="yo"),
    path('sup/<str:state>/',views.dis_view,name="sup"),
    path('searchtwitter/twit/',views.twitter,name="twitter"),
    path('searchtwitter/',views.searchtwitter,name="searchtwitter"),
]