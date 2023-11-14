
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone 

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    anio = models.IntegerField(verbose_name="Año",choices=[(year, year) for year in range(timezone.now().year - 1, timezone.now().year + 2)])
    activo = models.BooleanField(default=True)
    sorteo_realizado = models.BooleanField(default=False)
    fecha_ultimo_sorteo = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Santa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    destinatario = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='santa_destinatario')
    excepcion = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='santa_excepcion_obsequio')
    organizador = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"
    
class Participacion(models.Model):
    santa = models.ForeignKey(Santa, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('santa', 'evento')  # Esto garantiza que un Santa solo pueda estar una vez en cada evento

    def __str__(self):
        return f"{self.santa} en {self.evento}"
    
class Opcion(models.Model):
    paricipacion = models.ForeignKey(Participacion, on_delete=models.CASCADE)
    nombre_regalo = models.CharField(max_length=255)
    link = models.URLField()
    imagen = models.ImageField(upload_to='opciones_regalos/')

    def __str__(self):
        return self.nombre_regalo