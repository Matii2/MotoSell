from django.contrib.auth import logout, login as zaloguj
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from MotoSell.forms import PojazdForm
from .models import Pojazd


# strona główna
def index(request):
    return render(request, "MotoSellApp/index.html", {
        "uzytkownik": request.user
    })


# rejestracja nowego użytkownika
def rejestracja(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        uzytkownik = form.save()
        zaloguj(request, uzytkownik)
        return redirect("index")
    return render(request, "MotoSellApp/rejestracja.html", {"formularz_rejestracji": form})


# logowanie
def logowanie(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        zaloguj(request, form.get_user())
        return redirect("index")
    return render(request, "MotoSellApp/login.html", {"formularz_logowania": form})


# wylogowanie
@login_required
def wyloguj(request):
    logout(request)
    return redirect("index")


# dodawanie nowej oferty
@login_required
def kreator(request):
    form = PojazdForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        pojazd = form.save(commit=False)
        pojazd.uzytkownik = request.user
        if pojazd.czy_opublikowany:
            pojazd.data_publikacji = timezone.now().date()
        pojazd.save()
        return redirect("pojazdy")
    return render(request, "MotoSellApp/kreator.html", {"formularz_pojazdu": form})


# lista wszystkich pojazdów
def pojazdy(request):
    return render(request, "MotoSellApp/pojazdy.html", {
        "pojazdy_wszystkie": Pojazd.objects.all()
    })


# lista pojazdów zalogowanego użytkownika
@login_required
def moje_pojazdy(request):
    return render(request, "MotoSellApp/moje_pojazdy.html", {
        "pojazdy_wszystkie": Pojazd.objects.filter(uzytkownik=request.user)
    })


# szczegóły oferty
def oferta(request, pk):
    warunki = Q(pk=pk) & Q(czy_usuniety=False)
    if request.user.is_authenticated:
        warunki &= Q(czy_opublikowany=True) | Q(uzytkownik=request.user)
    else:
        warunki &= Q(czy_opublikowany=True)
    pojazd = get_object_or_404(Pojazd, warunki)
    return render(request, "MotoSellApp/oferta.html", {"pojazd": pojazd})


# ppublikacja oferty
@login_required
def publikuj(request, pk):
    pojazd = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    pojazd.czy_opublikowany = True
    pojazd.data_publikacji = timezone.now()
    pojazd.save()
    return redirect("oferta", pk=pk)


# cofnięcie publikacji
@login_required
def cofnij_publikacje(request, pk):
    pojazd = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    pojazd.czy_opublikowany = False
    pojazd.data_publikacji = None
    pojazd.save()
    return redirect("oferta", pk=pk)


# usunięcie oferty
@login_required
def usun(request, pk):
    pojazd = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    pojazd.czy_usuniety = True
    pojazd.save()
    return redirect("moje_pojazdy")


# edycja oferty
@login_required
def edytuj(request, pk):
    pojazd = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    form = PojazdForm(request.POST or None, request.FILES or None, instance=pojazd)
    if request.method == "POST" and form.is_valid():
        zmodyfikowany = form.save(commit=False)
        zmodyfikowany.uzytkownik = request.user
        if zmodyfikowany.czy_opublikowany and not zmodyfikowany.data_publikacji:
            zmodyfikowany.data_publikacji = timezone.now().date()
        zmodyfikowany.save()
        return redirect("oferta", pk=pk)
    return render(request, "MotoSellApp/edytuj.html", {"formularz_pojazdu": form})
