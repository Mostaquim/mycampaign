from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Messages

class MessageForm(forms.Form):
    subject = forms.CharField()
    text = forms.CharField(widget=SummernoteWidget())