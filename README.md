## FileShareApp - Filesharing system using django on aws lambda

### Description

FileShareApp is used to share the files across multiple users. Uploader can login and share the file to another user. Downloader will get notification via Email and user can download the file.

### Details

Framework - Django

Static files stored in s3

Database - S3 backed database

Deployed on AWS Lambda

Email Notification - Mailgun

### Steps used to deploy

step 1 : pip install -r requirements.txt 

step 2 : python manage.py runserver 

step 3 : zappa init

step 4 : zappa deploy dev

step 5 : python manage.py collectstatic --noinput

step 6 : python manage.py makemigrations

step 7 : zappa update dev

step 8 : zappa manage dev migrate

step 9 : zappa manage <stage> create_admin_user
  
Follow the below links to get more information.

#### References

lambda deploy using zappa - https://romandc.com/zappa-django-guide/
s3 backed db - https://github.com/Miserlou/zappa-django-utils

