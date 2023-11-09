from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import User 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Santa, Evento, Opcion
from .forms import SantaForm, EventoForm, OpcionInlineFormSet

import csv
import random
import logging

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        super().form_valid(form)
        return redirect('home')


class SantaCreateView(LoginRequiredMixin, CreateView):
    model = Santa
    form_class = SantaForm
    template_name = 'santa_form.html'
    success_url = reverse_lazy('ruta_a_la_pagina_de_evento') 



def asignar_destinatarios(santas):
    santas_copy = list(santas)
    destinatarios = []

    for santa in santas:
        # Filtra a los santas que cumplen con la restricción de excepción_obsequio (si está presente)
        if santa.excepcion_obsequio:
            santas_filtrados = [s for s in santas_copy if s != santa and s != santa.excepcion_obsequio]
        else:
            santas_filtrados = [s for s in santas_copy if s != santa]

        destinatario = random.choice(santas_filtrados)

        destinatarios.append(destinatario)
        santas_copy.remove(destinatario)

    # Actualiza los destinatarios en el modelo Santa
    for i, santa in enumerate(santas):
        santa.destinatario = destinatarios[i]
        santa.save()

    return destinatarios

def crea_santas_from_csv(evento, csv_file):
    # Define los nombres de campo requeridos en el CSV
    campos_requeridos = ['usuario', 'nombre', 'apellido', 'correo']
    # Lee el archivo CSV y verifica si contiene los campos requeridos
    try:
        csv_reader = csv.DictReader(csv_file)
    
        if all(campo in csv_reader.fieldnames for campo in campos_requeridos):
            for row in csv_reader:
                username = row['usuario']
                nombre = row['nombre']
                apellido = row['apellido']
                correo = row['correo']
                contraseña = row.get('contraseña', nombre)  # Valor predeterminado: nombre si contraseña está vacía

                # Crea o recupera al usuario
                user, created = User.objects.get_or_create(username=username, defaults={'first_name': nombre, 'last_name': apellido, 'email': correo})
                user.set_password(contraseña)
                user.save()

                # Verifica si el usuario fue creado o ya existía
                if created:
                    # Si el usuario es nuevo, envía un correo de notificación
                    subject = 'Bienvenido a nuestro evento de intercambio de regalos'
                    message = 'Has sido agregado como Santa para el evento "{}".'.format(evento.nombre)
                    from_email = 'noreply@example.com'
                    recipient_list = [user.email]  # Asume que los usuarios tienen un campo "email" en su modelo

                    send_mail(subject, message, from_email, recipient_list)

                # Crea o recupera al Santa y vincúlalo al evento
                santa, created = Santa.objects.get_or_create(usuario=user, eventos=evento)
            return {"respuesta": True, "mensaje": "Se agregaron los participantes"}
        else:
            return {"respuesta": False, "mensaje": "No tiene el formato adecuado"}
    
    except:
        return {"respuesta": False, "mensaje": "No se pudo leer el archivo"}


@login_required
def agregar_santas_desde_csv(request, pk):
    evento = get_object_or_404(Evento, pk=pk)    

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        mensaje_resultado = crea_santas_from_csv(evento, csv_file)
        print(mensaje_resultado)

        if mensaje_resultado.get("respuesta"):
            return render(request, 'actualizar_evento.html', {'mensaje': mensaje_resultado.get("mensaje"), "pk": evento.pk})
        else:       
            return render(request, 'agregar_santas_desde_csv.html', {'mensaje': mensaje_resultado.get("mensaje"), "evento": evento})

    return render(request, 'agregar_santas_desde_csv.html', {"evento": evento})


class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'lista_eventos.html'
    context_object_name = 'eventos'

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'agregar_evento.html'
    success_url = reverse_lazy('eventos')

class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'actualizar_evento.html'
    success_url = reverse_lazy('eventos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        eventos_activos = Evento.objects.filter(santa__usuario=self.request.user, activo=True)
        context['santas'] = evento.santa_set.all()
        context['eventos_activos'] = eventos_activos
        return context

class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'borrar_evento.html'
    success_url = reverse_lazy('eventos')


class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'detalle_evento.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        context['santas'] = evento.santa_set.all()
        return context

#### Sorteo

@login_required
def realizar_sorteo(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    santas = Santa.objects.filter(eventos=evento)

    # Lógica para realizar el sorteo
    asignar_destinatarios(santas)

    evento.sorteo_realizado = True
    evento.save()

    return redirect('detalle_evento', evento_id=evento_id)  # Redirige al detalle del evento

@login_required
def realizar_nuevo_sorteo(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)

    if evento.sorteo_realizado:
        # Si el sorteo ya se ha realizado, mostrar una confirmación o mensaje de advertencia
        messages.warning(request, 'El sorteo ya se ha realizado. ¿Deseas realizar un nuevo sorteo?')
    else:
        santas = Santa.objects.filter(eventos=evento)

        # Lógica para realizar un nuevo sorteo
        asignar_destinatarios(santas)

        evento.sorteo_realizado = True
        evento.save()

    return redirect('detalle_evento', evento_id=evento_id)  # Redirige al detalle del evento

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def inicio(request):
    if request.user.is_authenticated:
        eventos_activos = Evento.objects.filter(santa__usuario=request.user, activo=True)
        return render(request, 'auth/home.html', {'eventos_activos': eventos_activos})
    else:
        return render(request, 'auth/home.html')

@login_required
def mis_eventos(request):
    usuario_actual = request.user
    eventos_activos = Evento.objects.filter( activo=True)
    return render(request, 'mis_eventos.html', {'eventos_activos': eventos_activos})


######################## Santas

def SantaUpdateView(request, id_santa, id_evento):
    santa = get_object_or_404(Santa, pk=id_santa)
    evento = get_object_or_404(Evento, pk=id_evento)
    formset = OpcionInlineFormSet(instance=santa, queryset=Opcion.objects.filter(evento=evento))
    
    if request.method == 'POST':
        formset = OpcionInlineFormSet(request.POST, request.FILES, instance=santa)
        if formset.is_valid():
            formset.save()
            return redirect('detalle_evento', pk=evento.pk)
    if request.user == santa.usuario:
        return render(request, 'santas/detail_santa.html', {'santa': santa, 'opciones': opciones, 'evento': evento})
    else:
        return render(request, 'santas/update_santa.html', {'formset': formset, 'santa': santa, 'evento': evento})

def detalle_santa(request, id_santa, id_evento):
    santa = get_object_or_404(Santa, pk=id_santa)
    evento = get_object_or_404(Evento, pk=id_evento)
    opciones = Opcion.objects.filter(santa=santa, evento=evento)
    return render(request, 'santas/detail_santa.html', {'santa': santa, 'opciones': opciones, 'evento': evento})