from datetime import date  # Import the date module
from django import forms
from .models import Logement

class LogementForm(forms.ModelForm):
    date = forms.DateField(initial=date.today)  # Set the initial value to today's date
    class Meta:
        model = Logement
        fields = ['image','logement_type', 'localisation', 'description','contactinfo']  # Exclude 'user' field
