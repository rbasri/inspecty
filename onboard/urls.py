from django.urls import path
from . import views

app_name = 'onboard'

urlpatterns = [
	path('', views.index, name='index'),
	path('success', views.submitOnboard, name='submit_onboard'),
]