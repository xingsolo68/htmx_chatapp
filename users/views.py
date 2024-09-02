from django.shortcuts import render

from users.forms import EditProfileForm


def detail_view(request):
    profile = request.user.profile

    return render(request, "users/profile.html", {"profile": profile})


def edit_view(request):
    form = EditProfileForm()

    return render(request, "users/profile_edit.html", {"form": form})
