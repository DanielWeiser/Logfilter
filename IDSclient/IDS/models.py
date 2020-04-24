from django.db import models

class Log(models.Model):
    unit = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.SmallIntegerField()
    danger = models.SmallIntegerField()
    timestamp = models.DateTimeField()