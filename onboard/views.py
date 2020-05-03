from django.shortcuts import render
from django.utils import timezone
from .models import Partner
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER


def index(request):
	return render(request, 'onboard/onboard.html')

def submitOnboard(request):
	try:
		fname = request.POST['fname']
		lname = request.POST['lname']
		address = request.POST['address']
		city = request.POST['city']
		state = request.POST['state']
		zipcode = request.POST['zip']
		email = request.POST['email']
		phone_number = request.POST['phone_number']
		timestamp = timezone.now()

	except KeyError:
		return render(request, 'onboard/onboard.html')

	else:
		partner = Partner(
				fname=fname,
				lname=lname,
				address=address, 
				city=city, 
				state=state, 
				zipcode=zipcode,
				email=email, 
				phone_number=phone_number,
				timestamp=timestamp)
		partner.save()
		send_mail('New onboard request', str(partner), EMAIL_HOST_USER, [EMAIL_HOST_USER])

		return render(request, 'onboard/success.html')