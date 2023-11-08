from django import forms
from .models import Santa, Evento

class SantaForm(forms.ModelForm):
    class Meta:
        model = Santa
        fields = ['usuario', 'eventos', 'organizador']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'anio', 'activo']