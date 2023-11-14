from django import forms
from django.forms import inlineformset_factory
from .models import Santa, Evento, Opcion

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, Submit

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ('nombre_regalo', 'link', 'imagen')

class OpcionFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OpcionFormsetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Div(
                Div('nombre_regalo', css_class='col-md-8'),
                Div('imagen', css_class='col-md-4'),
                css_class='row',
            ),
            Div(
                Div('link', css_class='col-md-12'),
                css_class='row',
            ),
        )
        self.form_tag = False

# Inline formset para las opciones de un Santa

OpcionInlineFormSet = inlineformset_factory(
    Santa, Opcion, form=OpcionForm,
    extra=2,can_delete=True 
)


class SantaForm(forms.ModelForm):
    class Meta:
        model = Santa
        fields = ['usuario', 'organizador']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'anio', 'activo']