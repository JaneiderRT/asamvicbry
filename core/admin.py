from django.contrib import admin

from .models import (
    Tipo_Documento, 
    Apartamento, 
    Tipo_Persona, 
    Persona, 
    Pregunta, 
    Opcion, 
    Respuesta, 
    Estado_Encuesta, 
    Encuesta, 
    Estado_Asamblea, 
    Asamblea, 
    Rel_Asamblea_Asistente
)

# Inlines
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1


class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 1


class RelAsambleaAsistenteInline(admin.TabularInline):
    model = Rel_Asamblea_Asistente
    extra = 1


# Admin 
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [
        RespuestaInline,
    ]


class PreguntaAdmin(admin.ModelAdmin):
    inlines = [
        OpcionInline,
    ]


class AsambleaAdmin(admin.ModelAdmin):
    inlines = [
        RelAsambleaAsistenteInline,
    ]

admin.site.register(Tipo_Documento)
admin.site.register(Apartamento)
admin.site.register(Tipo_Persona)
admin.site.register(Persona)
admin.site.register(Pregunta, PreguntaAdmin)
#admin.site.register(Respuesta)
admin.site.register(Estado_Encuesta)
admin.site.register(Encuesta)
admin.site.register(Estado_Asamblea)
admin.site.register(Asamblea, AsambleaAdmin)
#admin.site.register(Rel_Asamblea_Asistente)