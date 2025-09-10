from django.urls import path
from django.contrib.auth import views as auth_views
from MotoSellApp import views

urlpatterns = [
    path('', views.lista_ofert, name='lista_ofert'),
    path('moje/', views.moje_oferty, name='moje_oferty'),
    path('dodaj/', views.dodaj_oferte, name='dodaj_oferte'),
    path('edytuj/<int:pk>/', views.edytuj_oferte, name='edytuj_oferte'),
    path('publikuj/<int:pk>/', views.publikuj_oferte, name='publikuj_oferte'),
    path('usun/<int:pk>/', views.usun_oferte, name='usun_oferte'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='MotoSell/login.html'), name='login'),
]
