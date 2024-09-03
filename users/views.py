from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse

from users.forms import EditProfileForm


def detail_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    return render(request, "users/profile.html", {"profile": profile})


def edit_view(request):
    form = EditProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect("users:profile")

    if request.path == reverse("users:onboarding"):
        template = "users/profile_onboarding.html"
    else:
        template = "users/profile_edit.html"

    return render(request, template, {"form": form})


def delete_view(request):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect("home")

    return render(request, "users/profile_delete.html")
