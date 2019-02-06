from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages
from .forms import UploadFileForm

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
                current_user = User.objects.get(id=request.session['id'])
                request.session['admin'] = current_user.admin
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
    t = Beat.objects.filter(user_id=request.session['id'])
    r = Beat.objects.filter(allowed_users=request.session['id'])
    context={
        "transfer": t,
        "recieved": r,

    }
    
    return render(request, 'beat_exchange/exchange.html', context)
#Upload
def upload(request):
    if "id" not in request.session:
        return redirect('/')
    context={
        "users": User.objects.exclude(id=request.session['id'])
    }
    return render(request, 'beat_exchange/upload.html', context)
def upload_process(request):
    def handle_uploaded_file(f):
        with open('media/filename', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    if "id" not in request.session:
        return redirect('/')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        formed = form.is_valid()
        if formed:
            handle_uploaded_file(request.FILES['file'])    
            user = User.objects.get(id=request.session['id'])
            Beat.objects.create(name=request.POST['name'], file_path=request.FILES['file'], desc=request.POST['desc'], user_id=user.id)
            beat=Beat.objects.last()
            for send_u in request.POST.getlist('send_user'):
                beat.allowed_users.add(send_u)
            return redirect('/review/'+str(beat.id))
    return redirect('/exchange')
def delete(request, id):
    d = Beat.objects.filter(id=id)
    d.delete()
    return redirect('/exchange')
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
def review(request, id):
    if "id" not in request.session:
        return redirect('/')
    context ={
        "upload": Beat.objects.get(id=id)
    }
    return render(request, 'beat_exchange/review.html', context)
#edit
def edit(request):
    response = "edit"
    return HttpResponse(response)
def edit_process(request):
    response = "edit_process"
    return HttpResponse(response)