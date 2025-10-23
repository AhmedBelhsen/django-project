from django.db import models
from ConferenceApp.models import Conference
# Create your models here.

class Session(models.Model):
    session_id=models.CharField(primary_key=True,max_length=8)
    title=models.CharField(max_length=100)
    topic=models.CharField(max_length=100)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    conference = models.ForeignKey( Conference, on_delete=models.CASCADE,  related_name="sessions" ) 
       
    def __str__(self):
        return self.title