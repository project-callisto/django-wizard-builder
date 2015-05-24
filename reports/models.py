from django.db import models

class Profile(models.Model):
    pass

class Report(models.Model):
    text = models.TextField(default='')
    profile = models.ForeignKey(Profile, default=None)