from django import forms
from django.contrib.auth.models import User

from .models import Apartamento, Persona, Asamblea

# DATA TYPE CLASS
class TypeDateAsamblea(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        self.format = '%Y-%m-%d'


class TypeTimeAsamblea(forms.TimeInput):
    input_type = 'time'


# CREATION CLASS
class CreateApartamento(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = [
            'nro_apartamento',
            'nro_torre'
        ]


class CreatePersona(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nro_documento',
            'tipo_documento',
            'nombres',
            'apellidos',
            'email',
            'nro_contacto',
            'tipo_persona',
            'usuario',
            'apartamento'
        ]


class CreateAsamblea(forms.ModelForm):
    class Meta:
        model = Asamblea
        exclude = [
            'id_asamblea',
            'usr_admin',
            'asistente',
            'estado'
        ]
        widgets = {
            'fecha_encuentro':TypeDateAsamblea,
            'hora_encuentro':TypeTimeAsamblea
        }


# UPDATE CLASS
class UpdateUsuario(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_active'
        ]


class UpdatePersona(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = [
            'nro_documento',
            'tipo_persona',
            'usuario',
            'apartamento'
        ]


class UpdateAsamblea(forms.ModelForm):
    class Meta:
        model = Asamblea
        exclude = [
            'id_asamblea',
            'usr_admin',
            'asistente'
        ]
        widgets = {
            'fecha_encuentro':TypeDateAsamblea,
            'hora_encuentro':TypeTimeAsamblea
        }