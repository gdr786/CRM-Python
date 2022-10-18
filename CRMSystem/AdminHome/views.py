import datetime
import random
import time

from bson import ObjectId
from connection import db
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import *
from django.shortcuts import render

admin_collection = db['admin']

# Auth again


def checkUser(request, admin_id):
    admin_details = admin_collection.find_one(ObjectId(admin_id))

    if bool(admin_details):
        request.session['userId'] = str(admin_details['_id'])
        return HttpResponseRedirect('/admin/admin-home')
    else:
        return HttpResponseRedirect('/admin-auth')

# dashboard


def home(request):
    if 'userId' not in request.session:
        return HttpResponseRedirect('/admin-auth')

    user_details = userDetails(request)
    context = {
        "user": user_details,
        "data": "",
    }
    return render(request, 'Admin-home/admin_base.html', context)

# ADMIN
# admin list


def adminList(request):
    if 'userId' not in request.session:
        return HttpResponseRedirect('/admin-auth')

    user_details = userDetails(request)
    if user_details['role'] == "admin":
        return HttpResponseRedirect('admin-home')

    admin_list = admin_collection.find()
    admin_list = objtodict(admin_list, False)
    context = {
        "user": user_details,
        "data": admin_list,
        "tableColumn": "0,1,2,3,4",
    }
    return render(request, 'Admin-home/admin_list.html', context)

# add admin


def addAdmin(request, id=0, type=""):
    if 'userId' not in request.session:
        return HttpResponseRedirect('/admin-auth')

    user_details = userDetails(request)
    context = {
        "user": user_details
    }
    if request.method == "POST":
        if id == 0:
            f_name = request.POST['fName']
            l_name = request.POST['lName']
            phone = request.POST['phone']
            email = request.POST['email']
            joining_date = convertDateFormat(
                request.POST['joiningDate'], '%Y-%m-%d')
            date_of_birth = convertDateFormat(
                request.POST['DateOfBirth'], '%Y-%m-%d')
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['role']
            status = int(request.POST['status'])
            imageFileName = uploadFile(request, 'image')

            insert_data = {
                "f_name": f_name,
                "l_name": l_name,
                "contact_no": phone,
                "email": email,
                "joining_date": joining_date,
                "image": imageFileName,
                "status": status,
                "password": password,
                "username": username,
                "DOB": date_of_birth,
                "role": role
            }

            x = admin_collection.insert_one(insert_data)
            return HttpResponseRedirect('/admin/admin-list')
        else:
            if type == "edit":
                return render(request, 'Admin-home/add_admin.html', context)
            else:
                return HttpResponseRedirect('/admin/admin-list')
    else:
        if id == 0:
            return render(request, 'Admin-home/add_admin.html', context)
        else:
            if type == "delete":
                delete_admin = admin_collection.delete_one(
                    {"_id": ObjectId(id)})
                return HttpResponseRedirect('/admin/admin-list')
            elif type == "edit":
                admin_detail = admin_collection.find_one({"_id": ObjectId(id)})
                admin_detail = objtodict(admin_detail, True)
                print(f"this is adimin : {admin_detail}")
                context['data'] = admin_detail
                context['is_edit'] = True
                return render(request, 'Admin-home/add_admin.html', context)
            else:
                return HttpResponseRedirect('/admin/admin-list')

# logout


def logout(request):
    del request.session['userId']
    return HttpResponseRedirect('/admin-auth')

# additional functions

# user details dict


def userDetails(request):
    uid = request.session['userId']
    admin_details = admin_collection.find_one(ObjectId(uid))
    user_details = {
        "userId": uid,
        "fName": admin_details['f_name'],
        "lName": admin_details['l_name'],
        "role": admin_details['role'],
        "contact": admin_details['contact_no'],
        "email": admin_details['email'],
        "image": admin_details['image'],
        "joiningDate": admin_details['joining_date'],
        "dateOfBirth": admin_details['DOB'],
    }
    return user_details

# convert object to dict


def objtodict(obj, is_one):
    if is_one:
        newdict = dict()
        newdict['id'] = str(obj['_id'])
        newdict['f_name'] = obj['f_name']
        newdict['l_name'] = obj['l_name']
        newdict['image'] = obj['image']
        newdict['contact_no'] = obj['contact_no']
        newdict['email'] = obj['email']
        newdict['username'] = obj['username']
        newdict['password'] = obj['password']
        newdict['role'] = obj['role']
        newdict['joining_date'] = obj['joining_date']
        newdict['DOB'] = obj['DOB']
        newdict['status'] = obj['status']
        return newdict
    else:
        newlist = list()
        for x in obj:
            subdict = dict()
            subdict['id'] = str(x['_id'])
            subdict['f_name'] = x['f_name']
            subdict['l_name'] = x['l_name']
            subdict['image'] = x['image']
            subdict['contact_no'] = x['contact_no']
            subdict['email'] = x['email']
            subdict['username'] = x['username']
            subdict['password'] = x['password']
            subdict['role'] = x['role']
            subdict['joining_date'] = x['joining_date']
            subdict['DOB'] = x['DOB']
            subdict['status'] = x['status']
            newlist.append(subdict)
        return newlist

# Function to convert string to datetime


def convertDateFormat(date_time, format):
    datetime_str = datetime.datetime.strptime(date_time, format)

    return datetime_str


# function for add files


def uploadFile(request, filename):
    image = request.FILES[filename] if filename in request.FILES else None
    if image:
        # create a new instance of FileSystemStorage
        fs = FileSystemStorage()
        # extract extention and create random name of file
        ext = (image.name).split(".")[-1].lower()
        randname = f"{random.randint(1111,9999)}-{round(time.time()*1000)}.{ext}"
        # save at requred location and give permitions of file size and etc
        file = fs.save(randname, image)
        # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        imageUrl = fs.url(file)
        return randname
    else:
        return ""
