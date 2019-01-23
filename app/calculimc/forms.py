from django import forms

class CalculImcForm(forms.Form):
    poids = forms.DecimalField(decimal_places=2,min_value=0.1)
    taille = forms.DecimalField(decimal_places=2,min_value=0.1)
