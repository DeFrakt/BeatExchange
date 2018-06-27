from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages

#User/Admin
def index(request):
    if "id" in request.session:
        request.session.flush()
    return render(request, 'beat_exchange/index.html')
def registration(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user_hash = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first'], last_name=request.POST['last'], email=request.POST['email'], password=user_hash)
            curr_user = User.objects.last()
            request.session['id'] = curr_user.id
            request.session['first_name'] = curr_user.first_name
            request.session['last_name'] = curr_user.last_name
            request.session['admin'] = curr_user.admin
            return redirect('/exchange')
    return redirect('/')
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            curr_user = User.objects.get(email=request.POST['email_login'])
            request.session['id'] = curr_user.id
            request.session['first_name'] = curr_user.first_name
            request.session['last_name'] = curr_user.last_name
            request.session['admin'] = curr_user.admin
            return redirect('/exchange')
    return redirect('/')
def admin(request):
    if "id" not in request.session:
        return redirect('/')
    elif request.session['admin'] == False:
        return redirect('/')
    context={
        "users": User.objects.all(),
        "beats": Beat.objects.all()
    }
    return render(request, 'beat_exchange/admin.html', context)
def admin_process(request):
    if request.method == "POST":
        if request.POST['action'] == "user":
            user = User.objects.get(email=request.POST['user'])
            request.session['admin_user'] = user.email
            request.session['admin_admin'] = user.admin
            request.session['admin_suspend'] = user.suspend
            return redirect('/admin')    
        elif request.POST['action'] == "user_update":
            user = User.objects.get(email=request.session['admin_user'])
            if request.POST['admin'] == "Yes":
                user.admin = True
                user.save()
                request.session['admin'] = True
            elif request.POST['admin'] == "No":
                user.admin = False
                user.save()
                request.session['admin'] = False
            if request.POST['suspend'] == "Yes":
                user.suspend = True
                user.save()
            elif request.POST['suspend'] == "No":
                user.suspend = False
                user.save()
            del request.session['admin_user']
            del request.session['admin_admin']
            del request.session['admin_suspend']
            return redirect('/admin')
    return redirect('/')
#Main Page
def exchange(request):
    if "id" not in request.session:
        return redirect('/')
    return render(request, 'beat_exchange/exchange.html')
#Upload
def upload(request):
    if "id" not in request.session:
        return redirect('/')
    return render(request, 'beat_exchange/upload.html')
def upload_process(request):
    response = "upload_process"
    return HttpResponse(response)
#Sampler
def sampler(request):
    if "id" not in request.session:
        return redirect('/')
    return render(request, 'beat_exchange/sample.html')
def sampler_process(request):
    response = "sampler_process"
    return HttpResponse(response)
#payment/stripe api
def cart(request):
    response = "cart"
    return HttpResponse(response)
def payment(request):
    response = "payment"
    return HttpResponse(response)
#Review
def review(request):
    response = "review"
    return HttpResponse(response)
#edit
def edit(request):
    response = "edit"
    return HttpResponse(response)
def edit_process(request):
    response = "edit_process"
    return HttpResponse(response)