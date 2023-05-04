from django import forms
from .models import News, Comment

class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = 'tags category title link date_off text'.split()
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date_off': forms.DateInput(attrs={
                'class': 'form-control'
            }),
            'text': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control'
            })
        }
