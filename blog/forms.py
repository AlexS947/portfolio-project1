from django import forms
from .models import Topic, Comment
from tinymce.widgets import TinyMCE

class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Topic
        fields = ['title', 'slug', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full max-w-md p-2 border rounded resize-y',
                'rows': 4,
                'placeholder': 'Write your comment here...',
            }),
        }
