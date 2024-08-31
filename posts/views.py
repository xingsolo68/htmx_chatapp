import requests
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render

from posts.forms import PostCreateForm

from .models import Post

# Create your views here.

def home_view(request):
  posts = Post.objects.all()

  return render(request, 'index.html', {"posts": posts})

def post_create_view(request):
  form = PostCreateForm()
  # body = json.loads(request.body)  

  if request.method == 'POST':
    form = PostCreateForm(request.POST)
    
    if form.is_valid():
      post = form.save(commit=False)

      website = requests.get(form.data['url'])
      
      sourcecode = BeautifulSoup(website.text, 'html.parser')

      post.save()
      return redirect('home')

  return render(request, 'posts/post_create.html', {"form" : form}) 
