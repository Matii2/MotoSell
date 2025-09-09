from django.db import models
from django.contrib.auth.models import User

class Samochod(models.Model):
    # Stałe słowniki
    CATEGORY_CHOICES = {
        'motocykl': 'Motocykl',
        'osobowy': 'Osobowy',
        'ciezarowy': 'Ciężarowy',
    }

    FUEL_CHOICES = {
        'benzyna': 'Benzyna',
        'diesel': 'Diesel',
        'lpg': 'LPG',
    }

    # Pola modelu
    tytul = models.CharField(max_length=255)
    opis = models.TextField()
    kategoria = models.CharField(
        max_length=20,
        choices=[(key, value) for key, value in CATEGORY_CHOICES.items()]
    )
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    rok_produkcji = models.PositiveIntegerField()
    przebieg = models.PositiveIntegerField(help_text="W kilometrach")
    pojemnosc_skokowa = models.PositiveIntegerField(help_text="W cm³")
    moc = models.PositiveIntegerField(help_text="W KM")
    rodzaj_paliwa = models.CharField(
        max_length=10,
        choices=[(key, value) for key, value in FUEL_CHOICES.items()]
    )
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    zdjecie = models.ImageField(upload_to='pojazdy/', null=True, blank=True)
    data_dodania = models.DateField(auto_now_add=True)
    data_publikacji = models.DateField(null=True, blank=True)

    usunieta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tytul} ({self.marka} {self.model})"