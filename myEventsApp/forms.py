from django import forms
from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('user', )
        fields = ('title', 'description', 'image', 'host', 'location', 'address', 'attendees', 'event_date')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control-file'}),
            'host': forms.TextInput(attrs={'placeholder': 'Host', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
            'attendees': forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control-number'}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

