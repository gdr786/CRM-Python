from django.shortcuts import render, redirect, reverse
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

# admin authantication check


def adminAuth(request):
    username_cookie = request.COOKIES.get('CRM-Auth-username')
    password_cookie = request.COOKIES.get('CRM-Auth-password')

    if username_cookie is None or password_cookie is None:
        if request.method == "POST":
            username = request.POST.get("login-email")
            password = request.POST.get("login-password")
            remember_me = request.POST.get("remember-me")

            query = {"username": username, "password": password}
            admin_details = admin_collection.find(query)
            # print(admin_details[0]['_id'])

            if (bool(admin_details)):
                response = HttpResponse(status=302)
                response['Location'] = f"admin/check/{admin_details[0]['_id']}"
                if remember_me:
                    set_cookie(response, key="CRM-Auth-username",
                               value=username, days_expire=30)
                    set_cookie(response, key="CRM-Auth-password",
                               value=password, days_expire=30)
                # redirect to home app for admin
                return response
            else:
                return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})

    else:
        query = {"username": username_cookie, "password": password_cookie}
        admin_details = admin_collection.find(query)
        if (bool(admin_details)):
            # redirect to home app for admin
            return HttpResponseRedirect(f"admin/check/{admin_details[0]['_id']}")
        else:
            return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})
    return render(request, 'login_admin.html')

# staff authantication check


def staffAuth(request):
    return render(request, 'login_staff.html')

# forget password process


def varifyMail(request):
    return render(request, 'varify_mail.html')

# set cookie using function added by gd


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 30 * 24 * 60 * 60  # one month
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
