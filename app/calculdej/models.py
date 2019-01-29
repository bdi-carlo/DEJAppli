from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    # nous avons 4 types : professionnelle, usuelle, loisir, sportive
    CATEGORIE_CHOICES = (
        ('Professionnelles', 'Professionnelles'),
        ('Usuelles', 'Usuelles'),
        ('Loisirs', 'Loisirs'),
        ('Sportives', 'Sportives'),
    )
    typeCat = models.CharField(
        max_length=16,
        choices=CATEGORIE_CHOICES,
    )


    def __str__(self):
        return self.nom

class Activite(models.Model):
    coef = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    titre = models.CharField(max_length=100)
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Dossier(models.Model):
    #titre = models.CharField(max_length=30,default="")
    date = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Date création")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dernier = models.BooleanField(default=True)

    def modif(self):
        self.dernier=False

class Travail(models.Model):
    dossierTrav = models.ForeignKey('Dossier', on_delete=models.CASCADE)
    categorieTrav = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    activiteTrav = models.ForeignKey('Activite', on_delete=models.CASCADE)
    dureeTrav = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
