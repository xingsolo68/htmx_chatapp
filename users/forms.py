from django import forms


from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "image": forms.FileInput(),
            "bio": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }
