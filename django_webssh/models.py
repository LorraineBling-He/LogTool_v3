from django.db import models

# Create your models here.
class Serverinfo(models.Model):
    name=models.CharField(max_length=64,unique=True)
    host=models.CharField(max_length=64)
    port=models.IntegerField()
    user=models.CharField(max_length=64)
    pwd=models.CharField(max_length=64)
    docker_name=models.CharField(max_length=64)
    create_time=models.DateTimeField(auto_now_add=True)
    is_del=models.IntegerField(default=0)
