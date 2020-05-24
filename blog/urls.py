from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path('', views.index, name='index'),
	path('post_1', views.post_1, name='post_1'),
	path('post_2', views.post_2, name='post_2'),
]