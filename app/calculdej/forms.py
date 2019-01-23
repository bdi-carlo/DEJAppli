from django import forms
from calculdej.models import Categorie, Activite, Dossier, Travail
from django.forms import formset_factory
from django.contrib.auth.models import User

class CalculDejForm(forms.Form):
    cat = forms.ModelChoiceField(queryset=Categorie.objects.all())
    act = forms.ModelChoiceField(queryset=None)
    duree = forms.DecimalField(decimal_places=2,min_value=0)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['act'].queryset = Activite.objects.none()

        if 'cat' in self.data:
            try:
                cat_t = Categorie(self.data.get('cat'))
                self.fields['act'].queryset = Activite.objects.filter(categorie=cat_t)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['act'].queryset = Activite.objects.none()

    def CatProfessionnelles(self):
        l = Categorie.objects.filter(typeCat='Professionnelles')
        self.fields['cat'].queryset = l

    def CatUsuelles(self):
        l = Categorie.objects.filter(typeCat='Usuelles')
        self.fields['cat'].queryset = l

    def CatLoisirs(self):
        l = Categorie.objects.filter(typeCat='Loisirs')
        self.fields['cat'].queryset = l

    def CatSportives(self):
        l = Categorie.objects.filter(typeCat='Sportives')
        self.fields['cat'].queryset = l

class CalculImcForm(forms.Form):
    poids = forms.DecimalField(decimal_places=2,min_value=0.0)
    taille = forms.DecimalField(decimal_places=2,min_value=0.0)

class SupprimerForm(forms.Form):
    pass
