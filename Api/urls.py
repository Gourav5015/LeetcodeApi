from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('api/',views.api,name="Api"),
    path('api/<str:username>/',views.api,name="api"),
]