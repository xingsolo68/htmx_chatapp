from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostCreateForm, PostEditForm, ReplyForm
from posts.utils import scrape_flickr

from .models import Comment, Post, Reply, Tag


def home_view(request, tag_slug=None):
    tag = ""
    if tag_slug:
        posts = Post.objects.filter(tags__slug=tag_slug)
        tag = get_object_or_404(Tag, slug=tag_slug)
    else:
        posts = Post.objects.all()

    return render(
        request,
        "posts/home.html",
        {"posts": posts, "tag": tag},
    )


def post_create_view(request):
    if request.method != "POST":
        return render(request, "posts/post_create.html", {"form": PostCreateForm()})

    form = PostCreateForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Form is not valid. Please check your input.")
        return render(request, "posts/post_create.html", {"form": form})

    post = form.save(commit=False)
    url = form.cleaned_data["url"]
    result = scrape_flickr(url)

    if result:
        post.image = result.get("image", "")
        post.title = result.get("title", "")
        post.artist = result.get("artist", "")

    post.author = request.user
    post.save()
    form.save_m2m()

    if result and all([post.image, post.title, post.artist]):
        messages.success(request, "Post created successfully with all data!")
    elif result:
        messages.warning(request, "Post created, but some data couldn't be scraped.")
    else:
        messages.error(
            request, "Failed to scrape data. Post created with form data only."
        )

    return redirect("home")


def post_delete_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")

        return redirect("home")

    return render(request, "posts/post_delete.html", {"post": post})


def post_edit_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostEditForm(instance=post)
    context = {"post": post, "form": form}

    if request.method == "POST":
        form = PostEditForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
            messages.success(request, "Post edited successfully")
            return redirect("home")

    return render(request, "posts/post_edit.html", context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentForm()
    replyform = ReplyForm()

    if request.htmx:
        if "top" in request.GET:
            comments = (
                post.comments.annotate(num_likes=Count("likes"))
                .filter(num_likes__gt=0)
                .order_by("-num_likes")
            )
        else:
            comments = post.comments.all()
        return render(
            request,
            "snippets/loop_postpage_comments.html",
            {"comments": comments, "replyform": replyform},
        )

    context = {
        "post": post,
        "commentform": commentform,
        "replyform": replyform,
    }

    return render(request, "posts/post_page.html", context)


def comment_sent(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    commentform = CommentForm(request.POST)
    replyform = ReplyForm()

    if request.method == "POST":
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    context = {"post": post, "comment": comment, "replyform": replyform}

    return render(request, "snippets/add_comment.html", context)


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)

    if request.method == "POST":
        comment.delete()
        return redirect("posts:detail", comment.post.id)

    return render(request, "posts/comment_delete.html", {"comment": comment})


def reply_sent(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    replyform = ReplyForm(request.POST)

    if request.method == "POST":
        if replyform.is_valid():
            reply = replyform.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()

    context = {"reply": reply, "comment": comment, "replyform": replyform}

    return render(request, "snippets/add_reply.html", context)


def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id, author=request.user)

    if request.method == "POST":
        reply.delete()
        return redirect("posts:detail", reply.comment.post.id)

    return render(request, "posts/reply_delete.html", {"reply": reply})


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get("pk"))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)

        return wrapper

    return inner_func


@like_toggle(Post)
def like_post(request, post):
    return render(request, "snippets/likes.html", {"post": post})


@like_toggle(Comment)
def like_comment(request, post):
    return render(request, "snippets/likes_comment.html", {"comment": post})


@like_toggle(Reply)
def like_reply(request, post):
    return render(request, "snippets/likes_reply.html", {"reply": post})
