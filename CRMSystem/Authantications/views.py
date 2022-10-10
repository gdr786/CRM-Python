from django.shortcuts import render, redirect, reverse
from django.http import *
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail


from bson import ObjectId
import datetime
import random,math
from connection import db

admin_collection = db['admin']
staff_collection = db['staff']


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
            admin_details = admin_collection.find_one(query)
            # print(admin_details[0]['_id'])

            if (bool(admin_details)):
                response = HttpResponse(status=302)
                response['Location'] = f"admin/check/{admin_details['_id']}"
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
        admin_details = admin_collection.find_one(query)
        if (bool(admin_details)):
            # redirect to home app for admin
            return HttpResponseRedirect(f"admin/check/{admin_details['_id']}")
        else:
            return render(request, 'login_admin.html', context={"errormsg": "Invalid username or password"})
    return render(request, 'login_admin.html')

# staff authantication check


def staffAuth(request):
    username_cookie = request.COOKIES.get('CRM-Auth-staff-username')
    password_cookie = request.COOKIES.get('CRM-Auth-staff-password')

    if username_cookie is None or password_cookie is None:
        if request.method == "POST":
            username = request.POST.get("login-email")
            password = request.POST.get("login-password")
            remember_me = request.POST.get("remember-me")

            query = {"username": username, "password": password}
            staff_details = staff_collection.find_one(query)

            if (bool(staff_details)):
                response = HttpResponse(status=302)
                response['Location'] = f"staff/check/{staff_details['_id']}"
                if remember_me:
                    set_cookie(response, key="CRM-Auth-staff-username",
                               value=username, days_expire=30)
                    set_cookie(response, key="CRM-Auth-staff-password",
                               value=password, days_expire=30)
                # redirect to home app for staff
                return response
            else:
                return render(request, 'login_staff.html', context={"errormsg": "Invalid username or password"})

    else:
        query = {"username": username_cookie, "password": password_cookie}
        staff_details = staff_collection.find_one(query)
        if (bool(staff_details)):
            # redirect to home app for staff
            return HttpResponseRedirect(f"staff/check/{staff_details['_id']}")
        else:
            return render(request, 'login_staff.html', context={"errormsg": "Invalid username or password"})
    return render(request, 'login_staff.html')

# forget password process


def varifyMail(request, type):
    if request.method == "POST":
        email = request.POST.get("forgot-password-email")

        if type == "admin":
            is_admin = admin_collection.find_one({"email": email})

            if bool(is_admin):
                otp = otpgen(6)
                mail_response = send_email(
                    "Reset Password", f"OTP : {otp}", email)

                request.session['admin_id'] = str(is_admin['_id'])
                request.session['otp'] = otp
                return HttpResponseRedirect('/forgot-password-step/admin')

            return render(request, 'varify_mail.html', context={"type": type, "errormsg": "Invalid Email Please Try Again!"})
        elif type == "staff":
            is_staff = staff_collection.find_one({"email": email})

            if bool(is_staff):
                otp = otpgen(6)
                mail_response = send_email(
                    "Reset Password", f"OTP : {otp}", email)

                request.session['staff_id'] = str(is_staff['_id'])
                request.session['otp'] = otp
                return HttpResponseRedirect('/forgot-password-step/staff')

            return render(request, 'varify_mail.html', context={"type": type, "errormsg": "Invalid Email Please Try Again!"})
        else:
            return render(request, 'varify_mail.html')

    return render(request, 'varify_mail.html', context={"type": type})

# forget password step varification


def forgetPassStep(request, type):
    if request.method == "POST":
        txt1 = request.POST.get("tx1")
        txt2 = request.POST.get("tx2")
        txt3 = request.POST.get("tx3")
        txt4 = request.POST.get("tx4")
        txt5 = request.POST.get("tx5")
        txt6 = request.POST.get("tx6")
        returnOtp = txt1 + txt2 + txt3 + txt4 + txt5 + txt6

        otp = request.session['otp']

        if otp == returnOtp:
            return HttpResponseRedirect(f'/change-password/{type}')
        else:
            return render(request, 'varify_otp.html', context={"type": type})

    else:
        return render(request, 'varify_otp.html', context={"type": type})


# resend otp


def resendOtpMail(request, type, uid):
    if type == "admin":
        is_admin = admin_collection.find_one({"_id": ObjectId(uid)})

        if bool(is_admin):
            otp = otpgen(6)
            mail_response = send_email(
                "Reset Password", f"OTP : {otp}", my_mail, is_admin['email'])
            print(mail_response)
            
            return render(request, 'varify_otp.html', context={"type": type, "crossotp": otp, "uid": is_admin['_id'], "email": is_admin['email']})

        return render(request, 'varify_mail.html', context={"type": type, "errormsg": "Invalid Email Please Try Again!"})
    elif type == "staff":
        is_staff = staff_collection.find_one({"_id": ObjectId(uid)})

        if bool(is_staff):
            otp = otpgen(6)
            mail_response = send_email("Reset Password", f"OTP : {otp}", is_staff['email'])
            print(mail_response)

            return render(request, 'varify_otp.html', context={"type": type, "crossotp": otp, "uid": is_staff['_id'], "email": is_staff['email']})

        return render(request, 'varify_mail.html', context={"type": type, "errormsg": "Invalid Email Please Try Again!"})

# change password


def changePassword(request, type):
    if request.method == "POST":
        new = request.POST.get("reset-password-new")
        new_confirm = request.POST.get("reset-password-confirm")
        if new == new_confirm:
            if type == "admin":
                admin_id = request.session['admin_id']
                admin_collection.update_one({"_id": ObjectId(admin_id)}, {"$set":{"password":new}})
                del request.session['admin_id']
                del request.session['otp']
                return HttpResponseRedirect('/admin-auth')
            elif type == "staff":
                staff_id = request.session['staff_id']
                admin_collection.update_one({"_id": ObjectId(staff_id)}, {"$set":{"password":new}})
                del request.session['staff_id']
                del request.session['otp']
                return HttpResponseRedirect('/staff-auth')
            else:
                return render(request, 'change_password.html', context={"type": type, "errormsg": "passwords don't match!"})

        else:
            return render(request, 'change_password.html', context={"type": type, "errormsg": "passwords don't match!"})
    else:
        return render(request, 'change_password.html', context={"type": type})


# ADDITIONAL FEAATURES
# set cookie using function added by gd


def set_cookie(response, key, value, days_expire=30):
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

# otp generator function 


def otpgen(length):
    otp=""
    for i in range(length):
        otp+=str(random.randint(1,9))
    return otp

# mail sender with security added by gd


def send_email(subject, message, to_email):
    
    if subject and message and to_email:
        try:
            send_mail(subject, message, 'hp0594137@gmail.com', [to_email])
        except BadHeaderError:
            return "Invalid header found."
        # return HttpResponseRedirect('/contact/thanks/')
        return "mail sent!"
    else:
        pass
        # handle validations and errors over here in real this function can 
