from django.core.urlresolvers import reverse
from django.db import models

class Profile(models.Model):
    def get_absolute_url(self):
        return reverse('view_profile', args=[self.id])

class Report(models.Model):
    text = models.TextField(default='')
    profile = models.ForeignKey(Profile, default=None)