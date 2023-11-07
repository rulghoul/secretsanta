
from django.contrib.auth.models import User
from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    año = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Santa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    eventos = models.ManyToManyField(Evento, through='Opciones')

    def __str__(self):
        return self.usuario.username

class Opciones(models.Model):
    santa = models.ForeignKey(Santa, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    nombre_regalo = models.CharField(max_length=255)
    link = models.URLField()
    imagen = models.ImageField(upload_to='opciones_regalos/')

    def __str__(self):
        return self.nombre_regalo