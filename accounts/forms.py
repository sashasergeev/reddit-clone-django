from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["about", "image"]
        widgets = {
            "about": forms.Textarea(
                attrs={
                    "cols": 80,
                    "class": "textarea-about",
                    "placeholder": "About (optional)",
                }
            )
        }
        labels = {"about": ""}
