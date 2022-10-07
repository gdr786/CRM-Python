from django.conf import settings
from django.http import *
from django.shortcuts import render

from bson import ObjectId
from connection import db

admin_collection = db['admin']

# Create your views here.
def checkUser(request, admin_id):
    admin_details = admin_collection.find_one(ObjectId(admin_id))
    
    return HttpResponse(f"this is home page with admin id: {admin_id}<br>user : {admin_details['f_name']} {admin_details['l_name']}")
