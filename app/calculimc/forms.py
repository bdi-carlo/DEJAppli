from django import forms

class CalculImcForm(forms.Form):
    poids = forms.DecimalField(decimal_places=2,min_value=0.1, label="Poids (en kg)")
    taille = forms.DecimalField(decimal_places=2,min_value=0.1, label="Taille (en cm)")
    age = forms.BooleanField(initial=False, label="J'ai 17 ans ou plus", required=False)
