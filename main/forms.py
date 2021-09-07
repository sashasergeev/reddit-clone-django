from django.forms import ModelForm
from .models import Comment
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "cols": 80,
                    "class": "post-comment-textarea",
                    "placeholder": "What are your thoughts?",
                }
            )
        }
        labels = {"text": ""}
