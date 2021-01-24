from django import forms
from django.forms.fields import EmailField


class DateInput(forms.DateInput):
    input_type = 'date'

class SelectDateForm(forms.Form):
    date = forms.DateField(widget=DateInput())

class SubmitForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=200, required=False)
