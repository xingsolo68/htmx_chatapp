from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostCreateForm, PostEditForm
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

def post_delete_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")

        return redirect('home')

    return render(request, 'posts/post_delete.html', {"post": post})

def post_edit_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostEditForm(instance=post)
    context = {'post': post, 'form': form }

    if request.method == "POST":
        form = PostEditForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Post edited successfully")
            return redirect('home')

    return render(request, 'posts/post_edit.html', context)

def post_page_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    return render(request, {"post": post})