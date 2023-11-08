from django.contrib import admin
from .models import Evento, Santa, Opcion

admin.site.index_title = 'Administrar Secret Santa'
admin.site.register(Evento)
admin.site.register(Santa)
admin.site.register(Opcion)