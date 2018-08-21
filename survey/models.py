from django.db import models

# Create your models here.

class Survey(models.Model):
	name = models.CharField(max_length=40)
	email = models.CharField(max_length=40)
	picture_list = models.CharField(max_length=10000)
	like_list = models.CharField(max_length=4000)
	id_code = models.IntegerField(default=0)
