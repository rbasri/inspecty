from django.shortcuts import render, get_object_or_404
from .models import Quote 
from django.utils import timezone
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER

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

	else:
		quote = Quote(address=address, 
					  city=city, 
					  state=state, 
					  zipcode=zipcode,
					  email=email, 
					  timestamp=timestamp,
					  options=quote_options)

		#Update this, get square feet and zestimate from zillow

		quote.getPrice()
		quote.save()
		#send_mail('New quote from ' + email, str(quote), EMAIL_HOST_USER, [EMAIL_HOST_USER])

		return render(request, 'rfq/quoted.html', {
			'quote': quote,
		})

def record(request, quote_id):
	#send_mail('New request to schedule inspection')
	quote = get_object_or_404(Quote, pk=quote_id)
	quote.scheduled=True
	quote.save()
	return render(request, 'rfq/record.html')