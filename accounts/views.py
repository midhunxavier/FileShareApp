from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import login as auth_login
from .models import FileShareAppUser
from files.models import FileItem
from django.core.files.storage import default_storage
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
import os
from django.conf import settings
import boto3
import requests
from django.core.mail import send_mail
from django.http import FileResponse



def send_simple_message(subject,message,email_from,to):
	return requests.post(
		"https://api.mailgun.net/v3/xxxxxxxxxxxxxxxxxxxxxxxxxxx.mailgun.org/messages",
		auth=("api", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
		data={"from": email_from,
			"to": to,
			"subject": subject,
			"text": message})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        #check if fields empty
        if username == "" or password == "": 
            return redirect('login')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else: 
            return redirect('login')
    
    else: 
        return render(request, 'pages/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
    return redirect('index')


def adduser(request):
    if request.user.is_superuser:
        if request.method == "POST":
        
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            role = request.POST['role']

            if role == "uploader":
                is_file_uploader = True
                is_file_downloader = False
            else:
                is_file_downloader = True
                is_file_uploader= False

                
            #check if fields empty
            if username == "" or password == "": 
                return render(request, 'dashboard-admin-adduser.html')
            
            else:

                user = FileShareAppUser.objects.create_user(username=username, password=password, email=email,
                is_file_uploader=is_file_uploader, is_file_downloader=is_file_downloader)
                
                user.save()
                
                return redirect('adminDashboard')

        else:   
            
            return render(request, 'pages/dashboard-admin-adduser.html')
    else:
        return redirect('dashboard')


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_file_uploader:
            return redirect('dashboardUploader')
        elif request.user.is_superuser:
            return redirect('adminDashboard')
        else:
            downloads = FileItem.objects.filter(file_downloader = request.user)

            context = {
                
                'files':downloads,

            }
            return render(request, 'pages/dashboard-downloader.html', context)
    else:
        return redirect('login')


def dashboardUploader(request):
    if request.user.is_authenticated:
        if request.user.is_file_uploader:
            
            return render(request, 'pages/dashboard-uploader.html')
        else:
            return redirect('dashboard')
    else:
        return redirect('login')


def upload(request):
    if request.user.is_file_uploader:
        if request.method == "POST":
            
            file_downloader = request.POST['file_downloader']
            if request.user.username == file_downloader:
                error = "File downloader can't be the File uploader. Please choose another username."

                context = {
                    'error': error,
                }
                
                return render(request, 'pages/dashboard-uploader.html', context)

            file_name = request.POST['file_name']
            file_desc = request.POST['file_desc']
            uploaded_file = request.FILES['file_file']

            try:
                file_downloaderuser = FileShareAppUser.objects.get(username = file_downloader)
            except:
                error = "User does not exist. Please choose another username."

                context = {
                    'error': error,
                }   
                return render(request, 'pages/dashboard-uploader.html', context)

            if not file_downloaderuser.is_file_downloader:
                error = "Recipient doesn't have permission to download. Please choose another username."

                context = {
                    'error': error,
                }
                
                return render(request, 'pages/dashboard-uploader.html', context)

            fileupload = FileItem(
                file_uploader=request.user,
                file_downloader = file_downloaderuser,
                file_file=uploaded_file,
                file_desc = file_desc,
                file_name=file_name,
            )
            fileupload.save()  

            subject = 'File Shared'
            message = 'Hi {0}, \n\nI have shared a file with you.\n\nRegards,\n{1}'.format(file_downloaderuser,request.user.username)
            email_from = request.user.email
            recipient_list = [file_downloaderuser.email,]
    

            try:
                send_simple_message(subject,message,email_from,recipient_list)

            except:
                return Response({'message': 'Recipient is not added to authorized maillist but file has uploaded'},status= HTTP_200_OK)

            return redirect('dashboardUploaderHistory')

        else:

            return redirect('dashboardUploader')
    else:
        return redirect('dashboard')

def download(request, file_id):
    if request.user.is_authenticated:
        download_file = FileItem.objects.get(id=file_id)
        if request.user == download_file.file_downloader or request.user == download_file.file_uploader:
            
            try: 
                s3 = boto3.client('s3')
                s3_object = s3.get_object(Bucket='zappa-56l2louf1', Key=download_file.file_file.name)
                body = s3_object['Body']
                response = HttpResponse(body.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + download_file.file_file.name

                return response
            except:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return HttpResponseForbidden('<h1>ACCESS DENIED</h1>')
    else:
        return redirect('login')



def dashboardUploaderHistory(request):
    if request.user.is_authenticated:
        if request.user.is_file_uploader:
            uploads = FileItem.objects.filter(file_uploader = request.user)

            context = {
                
                'files':uploads,

            }
            return render(request, 'pages/dashboard-uploader-history.html', context)
        else:
            return redirect('dashboard')
    else:
        return redirect('login')

def adminDashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users = FileShareAppUser.objects.all()

            context = {
                
                'users':users,

            }
            return render(request, 'pages/dashboard-admin.html', context)
        else:
            return redirect('dashboard')
    else:
        return redirect('login')