from django import forms
from .models import User
from django.core.exceptions import ObjectDoesNotExist

class LoginForm(forms.Form):
    email = forms.EmailField(help_text="Enter your email address")
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }


class QuotationForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    company_name = forms.CharField()
    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except ObjectDoesNotExist:
            user = None
        if user:
            raise forms.ValidationError("A user with the email already exists")
        return self.cleaned_data['email'].lower()
