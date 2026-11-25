from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaskDb(models.Model):

    user = models.ForeignKey(User,on_delete= models.CASCADE)
    title =models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date =models.DateField()
    status_choices = (
        ("pending","pending"),
        ("done","done")
    )
    status = models.CharField(max_length=100,choices=status_choices,default="pending")
