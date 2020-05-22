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
	def getPrice(self, sqft=0, year_built=0, home_value=0, unit_type=''):

		age = 2020-year_built
		quoted_price = 0

		cost_sqfoot = 400 + max(0,(sqft-3000)*0.1)
		cost_radon = 150
		cost_termite = 100
		cost_mold = 425
		cost_well = 100
		cost_pool = 150
		cost_age = age*0.5
		cost_value = home_value / 8000.0

		if 'base-inspect' in self.options:
			if 'APT' in str(unit_type):
				quoted_price += 250
			else:
				quoted_price += cost_sqfoot
		if 'radon' in self.options:
			quoted_price += cost_radon
		if 'termite' in self.options:
			quoted_price += cost_termite
		if 'mold' in self.options:
			quoted_price += cost_mold
		if 'well' in self.options:
			quoted_price += cost_well
		if 'pool' in self.options:
			quoted_price += cost_pool

		quoted_price += cost_age + cost_value

		self.price = int(quoted_price)