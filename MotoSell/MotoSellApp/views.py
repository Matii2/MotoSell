from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Pojazd
from MotoSell.forms import VehicleForm

def lista_ofert(request):
    oferty = Pojazd.objects.filter(data_publikacji__isnull=False, usunieta=False)
    return render(request, 'MotoSellApp/oferty/lista.html', {'oferty': oferty})

@login_required
def moje_oferty(request):
    oferty = Pojazd.objects.filter(uzytkownik=request.user, usunieta=False)
    return render(request, 'MotoSellApp/oferty/moje.html', {'oferty': oferty})

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
    return render(request, 'MotoSellApp/oferty/formularz.html', {'form': form})

@login_required
def edytuj_oferte(request, pk):
    oferta = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=oferta)
        if form.is_valid():
            form.save()
            return redirect('moje_oferty')
    else:
        form = VehicleForm(instance=oferta)
    return render(request, 'MotoSellApp/oferty/formularz.html', {'form': form})

@login_required
def publikuj_oferte(request, pk):
    oferta = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    oferta.data_publikacji = timezone.now()
    oferta.save()
    return redirect('moje_oferty')

@login_required
def usun_oferte(request, pk):
    oferta = get_object_or_404(Pojazd, pk=pk, uzytkownik=request.user)
    oferta.usunieta = True
    oferta.save()
    return redirect('moje_oferty')
