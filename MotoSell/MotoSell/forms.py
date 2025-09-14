from django import forms
from MotoSellApp.models import Pojazd

class PojazdForm(forms.ModelForm):
    class Meta:
        model = Pojazd
        exclude = ['uzytkownik', 'data_dodania', 'data_publikacji', 'usunieta']
