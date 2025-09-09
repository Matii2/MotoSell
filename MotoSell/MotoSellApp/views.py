from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Samochod
from MotoSell.forms import VehicleForm  # zakładamy, że masz formularz ModelForm

# a. Wszystkie opublikowane oferty
def lista_ofert(request):
    oferty = Samochod.objects.filter(data_publikacji__isnull=False, usunieta=False)
    return render(request, 'MotoSell/oferty/lista.html', {'oferty': oferty})

# b. Oferty zalogowanego użytkownika
@login_required
def moje_oferty(request):
    oferty = Samochod.objects.filter(uzytkownik=request.user, usunieta=False)
    return render(request, 'MotoSell/oferty/moje.html', {'oferty': oferty})

# c. Dodanie nowej oferty
@login_required
def dodaj_oferte(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.uzytkownik = request.user
            oferta.save()
            return redirect('moje_oferty')
    else:
        form = VehicleForm()
    return render(request, 'MotoSell/oferty/formularz.html', {'form': form})

# d. Edycja oferty (tylko własnej)
@login_required
def edytuj_oferte(request, pk):
    oferta = get_object_or_404(Samochod, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid():
            form.save()
            return redirect('moje_oferty')
    else:
        form = VehicleForm(instance=oferta)
    return render(request, 'MotoSell/oferty/formularz.html', {'form': form})

# e. Publikacja oferty
@login_required
def publikuj_oferte(request, pk):
    oferta = get_object_or_404(Samochod, pk=pk, uzytkownik=request.user)
    oferta.data_publikacji = timezone.now()
    oferta.save()
    return redirect('moje_oferty')

# f. Usunięcie oferty (oznaczenie jako usunięta)
@login_required
def usun_oferte(request, pk):
    oferta = get_object_or_404(Samochod, pk=pk, uzytkownik=request.user)
    oferta.usunieta = True
    oferta.save()
    return redirect('moje_oferty')
