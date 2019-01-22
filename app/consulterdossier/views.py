from django.shortcuts import render

@login_required
def consulterdossier(request):
    return render(request, 'calculdej/consulterdossier.html')
