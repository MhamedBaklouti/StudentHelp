# forms.py

from django import forms
from .models import Trajet

class TrajetForm(forms.ModelForm):
    class Meta:
        model = Trajet
        fields =  [ 'destination', 'point_depart','heure_depart','nb_places','contactinfo']
