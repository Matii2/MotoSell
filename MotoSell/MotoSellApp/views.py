from django.contrib.auth import login as zaloguj_uzytkownika, logout as wyloguj_uzytkownika
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from MotoSell.forms import PojazdForm
from .models import Pojazd


def strona_glowna(zadanie):
    return render(zadanie, "MotoSellApp/index.html", {"konto": zadanie.user})


def rejestruj(zadanie):
    formularz = UserCreationForm(zadanie.POST or None)
    if zadanie.method == "POST" and formularz.is_valid():
        zaloguj_uzytkownika(zadanie, formularz.save())
        return redirect("index")
    return render(zadanie, "MotoSellApp/rejestracja.html", {"formularz": formularz})


def loguj(zadanie):
    formularz = AuthenticationForm(zadanie, data=zadanie.POST or None)
    if zadanie.method == "POST" and formularz.is_valid():
        zaloguj_uzytkownika(zadanie, formularz.get_user())
        return redirect("index")
    return render(zadanie, "MotoSellApp/login.html", {"formularz": formularz})


@login_required
def wyloguj(zadanie):
    wyloguj_uzytkownika(zadanie)
    return redirect("index")


@login_required
def dodaj_oferte(zadanie):
    formularz = PojazdForm(zadanie.POST or None, zadanie.FILES or None)
    if zadanie.method == "POST" and formularz.is_valid():
        nowy_pojazd = formularz.save(commit=False)
        nowy_pojazd.wlasciciel = zadanie.user
        if nowy_pojazd.czy_opublikowany:
            nowy_pojazd.data_publikacji = timezone.now()
        nowy_pojazd.save()
        return redirect("pojazdy")
    return render(zadanie, "MotoSellApp/kreator.html", {"formularz": formularz})


def lista_pojazdow(zadanie):
    return render(zadanie, "MotoSellApp/pojazdy.html", {"pojazdy_wszystkie": Pojazd.objects.all()})


@login_required
def moje_oferty(zadanie):
    return render(zadanie, "MotoSellApp/moje_pojazdy.html", {"lista": Pojazd.objects.filter(uzytkownik=zadanie.user)})


def szczegoly_oferty(zadanie, identyfikator):
    filtr = Q(pk=identyfikator, czy_usuniety=False) & (
        Q(czy_opublikowany=True) | Q(uzytkownik=zadanie.user) if zadanie.user.is_authenticated else Q(czy_opublikowany=True)
    )
    pojazd = get_object_or_404(Pojazd, filtr)
    return render(zadanie, "MotoSellApp/info_oferta.html", {"pojazd": pojazd})


@login_required
def opublikuj(zadanie, identyfikator):
    pojazd = get_object_or_404(Pojazd, pk=identyfikator, uzytkownik=zadanie.user)
    pojazd.czy_opublikowany, pojazd.data_publikacji = True, timezone.now()
    pojazd.save()
    return redirect("info_oferta", pk=identyfikator)

@login_required
def cofnij_opublikowanie(zadanie, identyfikator):
    pojazd = get_object_or_404(Pojazd, pk=identyfikator, uzytkownik=zadanie.user)
    pojazd.czy_opublikowany, pojazd.data_publikacji = False, None
    pojazd.save()
    return redirect("info_oferta", pk=identyfikator)


@login_required
def oznacz_usuniety(zadanie, identyfikator):
    pojazd = get_object_or_404(Pojazd, pk=identyfikator, uzytkownik=zadanie.user)
    pojazd.czy_usuniety = True
    pojazd.save()
    return redirect("moje_pojazdy")


@login_required
def edytuj_oferte(zadanie, identyfikator):
    pojazd = get_object_or_404(Pojazd, pk=identyfikator, uzytkownik=zadanie.user)
    formularz = PojazdForm(zadanie.POST or None, zadanie.FILES or None, instance=pojazd)
    if zadanie.method == "POST" and formularz.is_valid():
        zmieniony = formularz.save(commit=False)
        zmieniony.uzytkownik = zadanie.user
        if zmieniony.czy_opublikowany and not zmieniony.data_publikacji:
            zmieniony.data_publikacji = timezone.now()
        zmieniony.save()
        return redirect("oferta", pk=identyfikator)
    return render(zadanie, "MotoSellApp/edytuj.html", {"formularz": formularz})
