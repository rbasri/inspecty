from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'blog/blog_home.html')

def post_1(request):
	return render(request, 'blog/post_1.html')