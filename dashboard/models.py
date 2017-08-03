from django.db import models

# Create your models here.

class PresentationURL(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.url

class DarkIceRunning(models.Model):
    running = models.BooleanField()

class ClarityRunning(models.Model):
    running = models.BooleanField()
