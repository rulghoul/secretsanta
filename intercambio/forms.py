from django import forms
from django.forms import inlineformset_factory
from .models import Santa, Evento, Opcion

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['nombre_regalo', 'link', 'imagen']

# Inline formset para las opciones de un Santa

OpcionInlineFormSet = inlineformset_factory(
    Santa, Opcion, form=OpcionForm,
    extra=2,can_delete=True 
)


class SantaForm(forms.ModelForm):
    class Meta:
        model = Santa
        fields = ['usuario', 'eventos', 'organizador']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'anio', 'activo']