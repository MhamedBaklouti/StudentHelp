from django.db import models
from study.models import Poste # type: ignore
from django.contrib.auth.models import User

class Trajet(Poste):
    TYPE_CHOICES = [
        (0, 'Offre'),
        (1, 'Demande'),
    ]
    conducteur = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    point_depart = models.CharField(max_length=100)
    heure_depart = models.TimeField()
    nb_places = models.IntegerField()
    contactinfo = models.CharField(max_length=100,default="+216")
    tranport_type = models.IntegerField(choices=TYPE_CHOICES,default=1)


    def __str__(self):
        return f"Trajet avec {self.conducteur} de {self.point_depart} à {self.destination}"
