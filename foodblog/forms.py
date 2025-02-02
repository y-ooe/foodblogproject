from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'コメントを入力してください',
        'rows': 4
    }))