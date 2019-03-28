from django.contrib import admin
from .models import Categorie, Activite, Dossier, Travail

class CategorieAdmin(admin.ModelAdmin):
   list_display   = ('nom','typeCat')
   list_filter    = ('nom',)
   ordering       = ('nom', )
   search_fields  = ('nom', 'typeCat')

class ActiviteAdmin(admin.ModelAdmin):
   list_display   = ('coef','categorie','titre')
   list_filter    = ('categorie',)
   ordering       = ('categorie', )
   search_fields  = ('titre', 'categorie')

class DossierAdmin(admin.ModelAdmin):
    list_display   = ('date','auteur','taille','poids','pathologie','age','sexe','de','det','imc','mb','niveau','dernier')
    list_filter    = ('auteur',)
    ordering       = ('auteur', )
    search_fields  = ('date', 'auteur')

class TravailAdmin(admin.ModelAdmin):
    list_display   = ('dossierTrav','categorieTrav','activiteTrav','dureeTrav','coefTrav')
    list_filter    = ('dossierTrav',)
    ordering       = ('dossierTrav',)
    search_fields  = ('dossierTrav',)

admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Travail, TravailAdmin)
