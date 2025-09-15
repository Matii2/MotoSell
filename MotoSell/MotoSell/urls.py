from django.urls import path
from django.contrib import admin
from MotoSellApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.strona_glowna, name='strona_glowna'),

    path('rejestracja/', views.rejestruj, name='rejestracja'),
    path('logowanie/', views.loguj, name='logowanie'),
    path('wyloguj/', views.wyloguj, name='wyloguj'),

    path('pojazdy/', views.lista_pojazdow, name='pojazdy'),
    path('moje-pojazdy/', views.moje_oferty, name='moje_pojazdy'),
    path('dodaj/', views.dodaj_oferte, name='dodaj_oferte'),
    path('oferta/<int:identyfikator>/', views.szczegoly_oferty, name='oferta'),
    path('edytuj/<int:identyfikator>/', views.edytuj_oferte, name='edytuj_oferte'),
    path('publikuj/<int:identyfikator>/', views.opublikuj, name='publikuj_oferte'),
    path('cofnij-publikacje/<int:identyfikator>/', views.cofnij_opublikowanie, name='cofnij_publikacje'),
    path('usun/<int:identyfikator>/', views.oznacz_usuniety, name='usun_oferte'),
]
