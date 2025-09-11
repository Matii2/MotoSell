from django import forms
from MotoSellApp.models import Samochod

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Samochod
        exclude = ['uzytkownik', 'data_dodania', 'data_publikacji', 'usunieta']
