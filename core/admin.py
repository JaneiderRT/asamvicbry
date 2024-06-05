from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth import get_user_model

from .models import Tipo_Documento, Apartamento, Tipo_Persona, Persona, Pregunta, Opcion, Respuesta, Encuesta, Estado_Asamblea, Asamblea, Rel_Asamblea_Asistente

# Register your models here.
'''
user = get_user_model()

class CustomUserAdmin(UserAdmin):
    pass
'''

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 1


class RelAsambleaAsistenteInline(admin.TabularInline):
    model = Rel_Asamblea_Asistente
    extra = 1


class UsuarioAdmin(admin.ModelAdmin):
    inlines = [
        RespuestaInline,
    ]


class AsambleaAdmin(admin.ModelAdmin):
    inlines = [
        RelAsambleaAsistenteInline,
    ]

admin.site.register(Tipo_Documento)
admin.site.register(Apartamento)
admin.site.register(Tipo_Persona)
admin.site.register(Persona)
admin.site.register(Pregunta)
admin.site.register(Opcion)
#admin.site.register(Usuario, UsuarioAdmin)
#admin.site.register(Respuesta)
admin.site.register(Encuesta)
admin.site.register(Estado_Asamblea)
admin.site.register(Asamblea, AsambleaAdmin)
#admin.site.register(Rel_Asamblea_Asistente)