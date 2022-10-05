from django.shortcuts import render, redirect
from django.http import *
from django.conf import settings

import datetime
import pymongo

# cluster connection
client = pymongo.MongoClient(
    'mongodb+srv://gdr:1231@testcluster.4fvy9vq.mongodb.net/?retryWrites=true&w=majority')
# database and collection connection
db = client['CRM_Python']
admin_collection = db['admin']


# Create your views here.
def index(request):
    return render(request, 'login_type.html')


def adminAuth(request):
    username_cookie = request.COOKIES.get('CRM-Auth-username')
    password_cookie = request.COOKIES.get('CRM-Auth-password')

    if username_cookie is None or password_cookie is None:
        if request.method == "POST":
            username = request.POST.get("login-email")
            password = request.POST.get("login-password")
            remember_me = request.POST.get("remember-me")

            query = {"username": username, "password": password}
            admin_count = admin_collection.count_documents(query)

            if (admin_count > 0):
                if remember_me:
                    print("this is in")
                    response = HttpResponse("set cokkie")
                    set_cookie(response, key="CRM-Auth-username",
                               value=username, days_expire=30)
                    set_cookie(response, key="CRM-Auth-password",
                               value=password, days_expire=30)

                # redirect to home app for admin
                username  = request.COOKIES.get('CRM-Auth-username')  
                password  = request.COOKIES.get('CRM-Auth-password')
                return render(request, 'login_admin.html')
            else:
                return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})

    else:
        query = {"username": username_cookie, "password": password_cookie}
        admin_count = admin_collection.count_documents(query)
        if (admin_count > 0):
            # redirect to home app for admin
            return render(request, 'login_admin.html')
        else:
            return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})
    username  = request.COOKIES.get('CRM-Auth-username')  
    password  = request.COOKIES.get('CRM-Auth-password')
    return render(request, 'login_admin.html', context ={"username": username, "password": password})


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
    return response
