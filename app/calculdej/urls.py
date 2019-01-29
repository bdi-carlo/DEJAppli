from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculdej, name='calculdej'),
    path('calculdejmb', views.calculdejmb, name='calculdejmb'),
    path('calculdejprofessionnelle', views.calculdejprofessionnelle, name='calculdejprofessionnelle'),
    path('calculdejusuelle', views.calculdejusuelle, name='calculdejusuelle'),
    path('calculdejloisir', views.calculdejloisir, name='calculdejloisir'),
    path('calculdejsport', views.calculdejsport, name='calculdejsport'),
    path('calculdejresultat', views.calculdejresultat, name='calculdejresultat'),
    path('load_act/', views.load_act, name='load_act'),
]
