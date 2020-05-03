from django.db import models

# Create your models here.

from django.utils import timezone

import datetime

class Quote(models.Model):
	address = models.CharField(max_length=200, default='')
	city = models.CharField(max_length=50, default='')
	state = models.CharField(max_length=20, default='')
	zipcode = models.CharField(max_length=10, default='')
	timestamp = models.DateTimeField()
	email = models.CharField(max_length=50, default='')
	price = models.IntegerField(default=0)
	options = models.CharField(max_length=200, default='')
	scheduled = models.BooleanField(default=False)

	def __str__(self):
		return self.email + ' | ' + str(self.timestamp)

	# Define regression for getting quote price
	def getPrice(self):

		#Dummy variables
		sqft = 1500.0
		age = 30
		quoted_price = 0

		cost_sqfoot = 450 + max(0,(sqft-3000)*0.1)
		cost_radon = 150
		cost_termite = 100
		cost_mold = 425
		cost_well = 100
		cost_pool = 150
		cost_age = age*0.5

		if 'base-inspect' in self.options:
			quoted_price += cost_sqfoot
		if 'radon' in self.options:
			quoted_price += cost_radon
		if 'termite' in self.options:
			quoted_price += cost_termite
		if 'mold' in self.options:
			quoted_price += cost_mold
		if 'well' in self.options:
			quoted_price += cost_well

		self.price = int(quoted_price)
