from django.contrib import messages
from django.shortcuts import redirect, render

from posts.forms import PostCreateForm
from posts.utils import scrape_flickr

from .models import Post


def home_view(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {"posts": posts})

def post_create_view(request):
    if request.method != 'POST':
        return render(request, 'posts/post_create.html', {"form": PostCreateForm()})

    form = PostCreateForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Form is not valid. Please check your input.")
        return render(request, 'posts/post_create.html', {"form": form})

    post = form.save(commit=False)
    url = form.cleaned_data['url']
    result = scrape_flickr(url)

    if result:
        post.image = result.get('image', '')
        post.title = result.get('title', '')
        post.artist = result.get('artist', '')

    post.save()

    if result and all([post.image, post.title, post.artist]):
        messages.success(request, "Post created successfully with all data!")
    elif result:
        messages.warning(request, "Post created, but some data couldn't be scraped.")
    else:
        messages.error(request, "Failed to scrape data. Post created with form data only.")

    return redirect('home')       
