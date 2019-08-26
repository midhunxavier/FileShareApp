from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.validators import RegexValidator
from django.utils import timezone


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'
 

class FileShareAppUser(AbstractUser):
    username = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric or contain numbers',
                           code='invalid_username'
                           )],
        unique=True 
    )

    email = models.CharField(max_length=50, blank=True, null=True)

    password = models.CharField(max_length=50, blank=True, null=True)
    
    is_file_uploader = models.BooleanField(default=False)

    is_file_downloader = models.BooleanField(default=False)


    def __str__(self):
        return self.username
