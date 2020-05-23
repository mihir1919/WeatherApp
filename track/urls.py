from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('tracker/',views.tracker,name="tracker"),
    path('tes/',views.tes,name="tes"),
    path('res/',views.res,name="res"),
    path('res/<str:city>/', views.resources,name="resources"),
    path('yo/<str:city>/',views.my_view,name="yo"),
]