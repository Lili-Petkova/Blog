from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'author')


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'short_text', 'full_text', 'status']


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    text = forms.CharField(max_length=1000, required=True)
