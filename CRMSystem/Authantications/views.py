from django.shortcuts import render
from django.http import *
from django.conf import settings

import datetime
import pymongo

# cluster connection 
client = pymongo.MongoClient('mongodb+srv://gdr:1231@testcluster.4fvy9vq.mongodb.net/?retryWrites=true&w=majority')
# database and collection connection
db = client['CRM_Python']
admin_collection = db['admin']


# Create your views here.
def index(request):
    return render(request, 'login_type.html')

def adminAuth(request):
    if request.method == "POST":
        username = request.POST["login-email"]
        password = request.POST["login-password"]
        remember_me = request.POST["remember-me"]

        query = {"username": username, "password": password}
        admin_count = admin_collection.count_documents(query)

        if(admin_count > 0):
            if remember_me:
                set_cookie(response, "CRM-Auth-username", username)
                set_cookie(response, "CRM-Auth-password", password)

            # redirect to home app for admin
            return render(request, 'login_admin.html')
        else:
            return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})
        
    return render(request, 'login_admin.html')

def staffAuth(request):
    return render(request, 'login_staff.html')

def varifyMail(request):
    return render(request, 'varify_mail.html')


# set cookie using function added by gd
def set_cookie(response, key, value, days_expire):
    if days_expire is None:
        max_age = 30 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )

    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        # domain=settings.SESSION_COOKIE_DOMAIN,
        # secure=settings.SESSION_COOKIE_SECURE or None,
    )