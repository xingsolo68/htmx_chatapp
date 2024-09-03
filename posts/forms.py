from django import forms
from django.forms import ModelForm

from posts.models import Comment, Post, Reply


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {"body": "Caption", "tags": "Category"}

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption ...",
                    "class": "font1 text-4xl",
                }
            ),
            "url": forms.TextInput(attrs={"placeholder": "Add url"}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {"body": "Caption", "tags": "Category"}

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption ...",
                    "class": "font1 text-4xl",
                }
            ),
            "url": forms.TextInput(attrs={"placeholder": "Add url"}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a comment ..."}
            ),
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a reply ..."}
            ),
        }
