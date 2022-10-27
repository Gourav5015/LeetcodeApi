import dataclasses
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from rest_framework.views import Response
from rest_framework.decorators import api_view
import json
from .leetcodeapi import LeetCodeApi
# Create your views here.
def home(request):
    return HttpResponse("Home")

def getData(username):
        user=LeetCodeApi(username=username)
        data={"NAME":user.getName(),"USERNAME":user.getUsername(),"RANK":user.getRank(),"URL":user.getProfileURL(),"STATS":(user.stats())}
        return data
@api_view(["GET"])
def api(request,username=None):
    data={}
    try:
        if (request.body):
            params=json.loads(request.body)
            username=params["username"]
            data=getData(username=username)
            return JsonResponse(data=data)
    except:
        return JsonResponse(data=data)
    if (request.GET.get("username")):
        username=request.GET.get("username")
        data=data=getData(username=username)
        return JsonResponse(data=data)
    if(username):
        data=data=getData(username=username)
    return JsonResponse(data=data)
    
