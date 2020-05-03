from django.urls import path
from . import views

app_name = 'rfq'

urlpatterns = [
	path('', views.index, name='index'),
	path('quoted', views.quoted, name='quoted'),
	path('record/<int:quote_id>', views.record, name='record'),
]