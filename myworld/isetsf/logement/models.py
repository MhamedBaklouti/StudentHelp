from django.db import models
from study.models import Poste # type: ignore

class Logement(Poste):
    TYPE_CHOICES = [
        (0, 'Offre'),
        (1, 'Demande'),
    ]
    localisation = models.CharField(max_length=100)
    contactinfo = models.CharField(max_length=100,default="+216 xx xxx xxx")
    logement_type = models.IntegerField(choices=TYPE_CHOICES,default=1)
   

    def __str__(self):
        return f"Logement  {self.localisation} : {self.contactinfo}"
