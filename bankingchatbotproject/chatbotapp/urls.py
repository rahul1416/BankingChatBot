from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name = "index"),
    path('getuser', views.getLogin, name='getLogin'),
    # path('getdetails', views.getDetails, name='getDetails'),
    path('sendaudio', views.sendaudio, name='sendaudio'),
    path('transfermoney', views.transferMoney, name='transfermoney'),
    path('sendtext',views.talktoOlama,name = 'talktoOlama'),
    path('sendOlama', views._response, name='_response'),
    path('tts',views._response,name='tts')
]
