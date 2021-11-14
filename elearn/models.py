from django.db import models
from django import forms
from django.contrib.auth.models import User
# from .utils import hash_file,upload_to
from .utils import upload_to
from .validators import validate_file_extension,validate_video_extension
#from .fields import RestrictedFileField
User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True
# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class SubjectSubscribe(models.Model):
    subjectid = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    subscribe = models.BooleanField(default=False)
    subscriber = models.ManyToManyField(User)

    def __str__(self):
        return self.subjectid


class Notification(models.Model):
    subjectid = models.ForeignKey(SubjectSubscribe , on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message


class Comments(models.Model):
    userID = models.ManyToManyField(User, related_name = 'user')
    subjectID = models.ManyToManyField(SubjectSubscribe)
    body = models.TextField()
    username = models.CharField(max_length=20,null=True)

    def __str__(self):
	    return f"User: {self.id} | Body: {self.body}"


class Video(models.Model):
    subjectid = models.ForeignKey(SubjectSubscribe, on_delete=models.CASCADE)
    videoname = models.CharField(max_length=100)
    attachment = models.FileField(upload_to=upload_to,validators=[validate_video_extension],null=True)
    #attachment = RestrictedFileField(upload_to='elearn/attachments/video/',content_types=['video/mp4'], max_upload_size=104857600,blank=True, null=True)
    uploader = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.subjectid

    def delete(self, *args, **kwargs):
        self.attachment.delete()
        super().delete(*args, **kwargs)

class File(models.Model):
    subjectid = models.ForeignKey(SubjectSubscribe, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    attachment = models.FileField(upload_to=upload_to,validators=[validate_file_extension],null=True)
    #attachment = RestrictedFileField(upload_to='elearn/attachments/file/',content_types=['application/pdf'],blank=True, null=True)
    uploader = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.subject

    def delete(self, *args, **kwargs):
        self.attachment.delete()
        super().delete(*args, **kwargs)