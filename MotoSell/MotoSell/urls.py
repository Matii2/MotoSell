from django.urls import path
from django.contrib import admin
from MotoSellApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('logowanie/', views.logowanie, name='logowanie'),
    path('wyloguj/', views.wyloguj, name='wyloguj'),

    path('pojazdy/', views.pojazdy, name='pojazdy'),
    path('moje-pojazdy/', views.moje_pojazdy, name='moje_pojazdy'),
    path('dodaj/', views.kreator, name='dodaj_oferte'),
    path('oferta/<int:pk>/', views.oferta, name='oferta'),
    path('edytuj/<int:pk>/', views.edytuj, name='edytuj_oferte'),
    path('publikuj/<int:pk>/', views.publikuj, name='publikuj_oferte'),
    path('cofnij-publikacje/<int:pk>/', views.cofnij_publikacje, name='cofnij_publikacje'),
    path('usun/<int:pk>/', views.usun, name='usun_oferte'),
]
