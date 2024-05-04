from django.db import models
from django import forms

# Create your models here.

class Response(models.Model):

    title           = models.CharField(max_length = 50)
    
    leader          = models.CharField(max_length = 50)
    leader_email    = models.EmailField()

    member2         = models.CharField(max_length = 50)
    member3         = models.CharField(max_length = 50)
    member4         = models.CharField(max_length = 50)

    abstract        = models.TextField()


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['title', 'leader', 'leader_email', 'member2',
                  'member3', 'member4', 'abstract']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'id': 'title', 'placeholder': 'Project Title', 'requierd': True}),
            'leader': forms.TextInput(attrs={'class': 'input-field', 'id': 'team-leader-email', 'placeholder': 'Name', 'requierd': True}),
            'leader_email': forms.EmailInput(attrs={'class': 'input-field', 'id': 'team-leader-email', 'placeholder': 'Email', 'required': True}),
            'member2': forms.TextInput(attrs={'class': 'input-field', 'id': 'project-team', 'placeholder': 'Member 2', 'required': True}),
            'member3': forms.TextInput(attrs={'class': 'input-field', 'id': 'project-team', 'placeholder': 'Member 3', 'required': True}),
            'member4': forms.TextInput(attrs={'class': 'input-field', 'id': 'project-team', 'placeholder': 'Member 4', 'required': True}),
            'abstract': forms.Textarea(attrs={'class': 'textarea-field', 'id': 'abstract', 'placeholder': 'Project Abstract', 'required': True})
        }
        