from django.shortcuts import render
from .forms import CalculImcForm
from django.contrib.auth.decorators import login_required


@login_required
def calculimc(request):
    formImc = CalculImcForm(request.POST or None)
    if formImc.is_valid():
        poids = formImc.cleaned_data['poids']
        taille = formImc.cleaned_data['taille']
        imc = round(poids/(taille*taille),2)
    return render(request, 'calculimc/calculimc.html', locals())
