from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'login_type.html')

def adminAuth(request):
    return render(request, 'login_admin.html')

def staffAuth(request):
    return render(request, 'login_staff.html')

def varifyMail(request):
    return render(request, 'varify_mail.html')