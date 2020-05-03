from django.db import models
import datetime
# Create your models here.

class Partner(models.Model):
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=20)
	zipcode = models.CharField(max_length=10)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)	
	timestamp = models.DateTimeField()

	def __str__(self):
		return self.fname + ' ' + self.lname