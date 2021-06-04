from django.shortcuts import render, get_object_or_404
from .models import Quote 
from django.utils import timezone
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
import requests

# Create your views here.
def index(request):
	return render(request, 'rfq/quotepage.html')

def quoted(request):
	options = ['base-inspect', 'radon', 'termite', 'mold', 'well', 'pool']
	#fetch form information out of the request
	#need to throw error if page accessed directly, i.e. no POST request
	try:
		address = request.POST['address']
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zip']
		email = request.POST['email']
		timestamp = timezone.now()
		quote_options = ''

		for option in options:
			if option in request.POST:
				quote_options+= option + ', '

	except KeyError:
		return render(request, 'rfq/quotepage.html')

	quote = Quote(address=address, 
				  city=city, 
				  state=state, 
				  zipcode=zipcode,
				  email=email, 
				  timestamp=timestamp,
				  options=quote_options)

	# endpoint = 'https://sandbox.estated.com/v4/property?' #sandbox
	endpoint = 'https://apis.estated.com/v4/property?' #production
	# token = 'HrKD9Ef6Rot4Yb9rxeDAfZdWKCiofs' #sandbox
	token = '' #production
	endpoint += 'token=' + token + '&combined_address='


	endpoint += address + ', ' + city + ', ' + state + ' ' + zipcode

	response = requests.get(endpoint)
	
	try:
		yr_built = response.json()['data']['structure']['year_built']
		sqft = response.json()['data']['structure']['total_area_sq_ft']
		home_value = response.json()['data']['valuation']['value']
		unit_type = response.json()['data']['address']['unit_type']

	except TypeError:
		error_message = "Sorry, we couldn't find that property. Try quoting again."
		return render(request, 'rfq/error.html', {'error' : error_message,})
	
	quote.getPrice(sqft=sqft, year_built=yr_built, home_value=home_value, unit_type=unit_type)
	quote.save()
	send_mail('New quote from ' + email, str(quote), EMAIL_HOST_USER, [EMAIL_HOST_USER])

	return render(request, 'rfq/quoted.html', {
		'quote': quote,
	})

def record(request):
	try:
		quote_id = request.POST['quote_id']

	except KeyError:
		error_message = "Sorry, something went wrong in trying to schedule that quote. Please try again."
		return render(request, 'rfq/error.html', {'error' : error_message})

	quote = get_object_or_404(Quote, pk=quote_id)

	send_mail('New request to schedule inspection', 'Quote ID = ' + str(quote_id), EMAIL_HOST_USER, [EMAIL_HOST_USER])
	quote.scheduled=True
	quote.save()
	return render(request, 'rfq/record.html')
