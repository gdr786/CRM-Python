from django.conf import settings
from django.http import *
from django.shortcuts import render

from bson import ObjectId
from connection import db

admin_collection = db['admin']

# Create your views here.
def checkUser(request, admin_id):
    admin_details = admin_collection.find_one(ObjectId(admin_id))
    print(admin_details)

    if bool(admin_details):
        request.session['userId'] = str(admin_details['_id'])
        return HttpResponseRedirect('/admin/admin-home')
    else:
        return HttpResponseRedirect('/admin-auth')

def home(request):
    if 'userId' not in request.session:
        return HttpResponseRedirect('/admin-auth')
    else:
        uid = request.session['userId']
        return HttpResponse(f"this is home and uis :{uid}")
