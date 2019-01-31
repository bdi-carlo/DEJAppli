from django import forms
from calculdej.models import Categorie, Activite, Dossier, Travail
from django.forms import formset_factory
from django.contrib.auth.models import User

class CalculDejForm(forms.Form):
    cat = forms.ModelChoiceField(label="Catégorie", queryset=Categorie.objects.all())
    act = forms.ModelChoiceField(label="Activité", queryset=None)
    duree = forms.DecimalField(label="Durée (h)", decimal_places=2,min_value=0)
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
        lc = Categorie.objects.filter(typeCat='Professionnelles')
        c = lc.reverse()[0]
        la = Activite.objects.filter(categorie=c)
        self.fields['cat'].queryset = lc
        self.fields['cat'].empty_label = None
        self.fields['act'].queryset = la



    def CatUsuelles(self):
        lc = Categorie.objects.filter(typeCat='Usuelles')
        c = lc.reverse()[0]
        la = Activite.objects.filter(categorie=c)
        self.fields['cat'].queryset = lc
        self.fields['cat'].empty_label = None
        self.fields['act'].queryset = la

    def CatLoisirs(self):
        l = Categorie.objects.filter(typeCat='Loisirs')
        self.fields['cat'].queryset = l

    def CatSportives(self):
        l = Categorie.objects.filter(typeCat='Sportives')
        self.fields['cat'].queryset = l

class CalculMBForm(forms.Form):
    CHOICES=[('M','M'),
             ('F','F'),
                 ]
    sexe = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    poids = forms.DecimalField(decimal_places=2,min_value=0.0)
    taille = forms.DecimalField(decimal_places=2,min_value=0.0)
    age = forms.IntegerField(min_value=0)

class DeplacementForm(forms.Form):
    dureelentsansport = forms.DecimalField(initial=0, label="Lent sans port de charge",decimal_places=2,min_value=0)
    dureemoderesansport = forms.DecimalField(initial=0, label="Modéré sans port de charge",decimal_places=2,min_value=0)
    dureemodereavecport = forms.DecimalField(initial=0, label="Modéré avec port de charge",decimal_places=2,min_value=0)
    dureeintense = forms.DecimalField(initial=0, label="Intense",decimal_places=2,min_value=0)

    def initialval(self):
        self.fields['dureelentsansport'] = 0
        self.fields['dureemoderesansport'] = 0
        self.fields['dureemodereavecport'] = 0
        self.fields['dureeintense'] = 0
