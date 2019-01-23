from django.shortcuts import render
from calculdej.models import Categorie
from calculdej.models import Activite
from calculdej.models import Dossier
from calculdej.models import Travail
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


# def check_user(user):
#     if user.is_authenticated:
#         username = user.get_username()
#
#     return username=='admin'

@login_required
# @user_passes_test(check_user)
def consulterdossier(request):
    dossiers = Dossier.objects.filter(auteur=request.user)
    return render(request, 'consulterdossier/consulterdossier.html', locals())
