from django.forms import ModelForm
from .models import Comment, Subreddit
from django import forms
from mptt.forms import TreeNodeChoiceField


class CommentForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].widget.attrs.update({"class": "d-none"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        model = Comment
        fields = ["text", "parent"]
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


class SubredditUpdateForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ["description", "image"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "cols": 80,
                    "class": "textarea-about",
                    "placeholder": "About (optional)",
                }
            )
        }
        labels = {"about": ""}
