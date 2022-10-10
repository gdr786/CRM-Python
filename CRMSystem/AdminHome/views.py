from django.conf import settings
from django.http import *
from django.shortcuts import render

from bson import ObjectId
from connection import db

admin_collection = db['admin']

# Create your views here.
def checkUser(request, admin_id):
    admin_details = admin_collection.find_one(ObjectId(admin_id))

    if bool(admin_details):
        request.session['otp'] = otp
    else:
        return HttpResponseRedirect('/admin-auth')
