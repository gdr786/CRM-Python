from django.conf import settings
from django.http import *
from django.shortcuts import render

import pymongo
from bson import ObjectId
# cluster connection
client = pymongo.MongoClient(
    'mongodb+srv://gdr:1231@testcluster.4fvy9vq.mongodb.net/?retryWrites=true&w=majority')
# database and collection connection
db = client['CRM_Python']
admin_collection = db['admin']

# Create your views here.
def checkUser(request, admin_id):
    admin_details = admin_collection.find_one(ObjectId(admin_id))
    
    return HttpResponse(f"this is home page with admin id: {admin_id}<br>user : {admin_details['f_name']} {admin_details['l_name']}")
