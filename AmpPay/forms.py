# forms.py
from django import forms

class PredictionForm(forms.Form):
    datetime = forms.DateTimeField(label='Enter Date and Time', input_formats=['%Y-%m-%d %H:%M:%S'])
