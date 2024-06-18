from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .admin import EncuestaAdmin

from .forms import (
    CreateApartamento,
    CreatePersona,
    CreateAsamblea,
    CreateEncuesta,
    UpdateUsuario,
    UpdatePersona,
    UpdateAsamblea,
    UpdateEncuesta
)

from .models import (
    Persona,
    Asamblea,
    Encuesta,
    Estado_Asamblea,
    Estado_Encuesta,
    Rel_Asamblea_Asistente,
    Rel_Encuesta_Pregunta,
    Apartamento
)

# AUTHENTICATION VIEWS
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user     = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {'error':'¡Ups! Revisa tus credenciales.'})

        login(request, user)

        if user.is_superuser:
            return redirect('home')

        return redirect('usrs_normales')

    return render(request, 'login.html')


@login_required
def singout(request):
    logout(request)
    return redirect('index')


# CREATION VIEWS
@login_required
@permission_required('core.add_apartamento', raise_exception=True)
def create_apartamentos(request):
    if request.method == 'POST':
        form_apartamento = CreateApartamento(request.POST)

        if not form_apartamento.is_valid():
            return render(request, 'creation_forms.html', {
                'title': 'Creación De Apartamentos',
                'form': CreateApartamento,
                'error': 'Inconveniente al crear el apartamento.'
            })

        form_apartamento.save(commit=True)
        return redirect('home')

    return render(request, 'creation_forms.html', {
        'title': 'Creación Apartamento',
        'form': CreateApartamento
    })


def create_encuestas(request):
    if request.method == 'POST':
        form_encuesta = CreateEncuesta(request.POST)

        if not form_encuesta.is_valid():
            return render(request, 'creation_forms.html', {
                'title': 'Creación Encuesta',
                'form': CreateEncuesta,
                'error': 'Inconveniente al crear la encuesta.'
            })
        
        new_encuesta = form_encuesta.save(commit=False)
        new_encuesta.estado = Estado_Encuesta.objects.get(abreviatura='INACT')
        new_encuesta.save()
        return redirect('encuestas')

    return render(request, 'creation_forms.html', {
        'title': 'Creación Encuesta',
        'form': CreateEncuesta
    })


@login_required
@permission_required('auth.add_user', raise_exception=True)
def create_users(request):
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return render(request, 'creation_forms.html', {
                    'title': 'Creación De Usuarios',
                    'form': UserCreationForm,
                    'error': 'El usuario ha sido creado'
                })
        except:
            return render(request, 'creation_forms.html', {
                'title': 'Creación De Usuarios',
                'form': UserCreationForm,
                'error': 'Inconveniente al crear el usuario.'
            })

    return render(request, 'creation_forms.html', {
        'title': 'Creación De Usuarios',
        'form': UserCreationForm
    })


@login_required
@permission_required('core.add_persona', raise_exception=True)
def create_personas(request):
    if request.method == 'POST':
        form_persona = CreatePersona(request.POST)

        if not form_persona.is_valid():
            return render(request, 'creation_forms.html', {
                'title': 'Creación De Personas',
                'form': CreatePersona,
                'error': 'Inconveniente al crear la persona.'
            })

        new_persona  = form_persona.save(commit=False)
        new_persona.save()
        return redirect('personas')

    return render(request, 'creation_forms.html', {
        'title': 'Creación De Personas',
        'form': CreatePersona
    })


@login_required
@permission_required('core.add_asamblea', raise_exception=True)
def create_asambleas(request):
    if request.method == 'POST':
        form_asamblea = CreateAsamblea(request.POST)

        if not form_asamblea.is_valid():
            return render(request, 'creation_forms.html', {
                'title': 'Creación De Asambleas',
                'form': CreateAsamblea,
                'error': 'Inconveniente al crear la asamblea.'
            })

        new_asamblea = form_asamblea.save(commit=False)
        new_asamblea.usr_admin = request.user
        new_asamblea.estado = Estado_Asamblea.objects.get(abreviatura='PEN')
        new_asamblea.save()
        return redirect('asambleas')

    return render(request, 'creation_forms.html', {
        'title': 'Creación De Asambleas',
        'form': CreateAsamblea
    })


# UPDATE VIEWS
def update_encuestas(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    EncuestaInlineFormSet = inlineformset_factory(Encuesta, Rel_Encuesta_Pregunta, fields=['pregunta'], can_delete=True, extra=1)

    if request.method == 'POST':
        try:
            form_encuesta = UpdateEncuesta(request.POST, instance=encuesta)
            encuesta_formset = EncuestaInlineFormSet(request.POST, request.FILES, instance=encuesta)
            form_encuesta.save()

            if encuesta_formset.is_valid():
                encuesta_formset.save()

            return redirect('encuestas')
        except:
            return render(request, 'update_encuestas.html', {
                'encuesta': encuesta,
                'form_encuesta': form_encuesta,
                'encuesta_formset': encuesta_formset,
                'error': 'No se pudo editar la información de la encuesta.'
            })
    
    form_encuesta = UpdateEncuesta(instance=encuesta)
    encuesta_formset = EncuestaInlineFormSet(instance=encuesta)
    return render(request, 'update_encuestas.html', {
        'encuesta': encuesta,
        'form_encuesta': form_encuesta,
        'encuesta_formset': encuesta_formset
    })


def update_users(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        try:
            form_usuario = UpdateUsuario(request.POST, instance=usuario)
            form_usuario.save()
            return redirect('usuarios')
        except:
            return render(request, 'update_usuarios.html', {
                'usuario': usuario,
                'form_usuario': form_usuario,
                'error': 'No se pudo editar la información del usuario.'
            })

    form_usuario = UpdateUsuario(instance=usuario)
    return render(request, 'update_usuarios.html', {
        'usuario': usuario,
        'form_usuario': form_usuario
    })


@login_required
@permission_required('core.change_persona', raise_exception=True)
def update_personas(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)

    if request.method == 'POST':
        try:
            form_persona = UpdatePersona(request.POST, instance=persona)
            form_persona.save()
            return redirect('personas')
        except:
            return render(request, 'update_personas.html', {
                'persona': persona,
                'form_persona': form_persona,
                'error': 'No se pudo editar la información de la persona.'
            })

    form_persona = UpdatePersona(instance=persona)
    return render(request, 'update_personas.html', {
        'persona': persona,
        'form_persona': form_persona
    })


@login_required
@permission_required('core.change_asamblea', raise_exception=True)
def update_asambleas(request, asamblea_id):
    asamblea = get_object_or_404(Asamblea, pk=asamblea_id)
    AsambleaInlineFormSet = inlineformset_factory(Asamblea, Rel_Asamblea_Asistente, fields=['asistente'], can_delete=True, extra=1)

    if request.method == 'POST':
        try:
            form_asamblea = UpdateAsamblea(request.POST, instance=asamblea)
            asamblea_formset = AsambleaInlineFormSet(request.POST, request.FILES, instance=asamblea)
            form_asamblea.save()

            if request.POST['rel_asamblea_asistente_set-0-asistente'] != '':
                if (int(request.POST['estado']) != 4) and (int(request.POST['estado']) != 5): #Asamblea No Esta En Estado De Ejecucion O Terminada
                    return render(request, 'update_asambleas.html', {
                    'asamblea': asamblea,
                    'form_asamblea': form_asamblea,
                    'asamblea_formset':asamblea_formset,
                    'error': 'La asamblea no se encuentra en ejecución.'
                })

                if asamblea_formset.is_valid():
                    asamblea_formset.save()

            return redirect('asambleas')
        except:
            return render(request, 'update_asambleas.html', {
                'asamblea': asamblea,
                'form_asamblea': form_asamblea,
                'asamblea_formset':asamblea_formset,
                'error': 'No se pudo editar la información de la asamblea.'
            })

    form_asamblea = UpdateAsamblea(instance=asamblea)
    asamblea_formset = AsambleaInlineFormSet(instance=asamblea)
    return render(request, 'update_asambleas.html', {
        'asamblea':asamblea,
        'form_asamblea':form_asamblea,
        'asamblea_formset':asamblea_formset
    })


# CONSULTATION VIEWS
def usuarios(request):
    users_list = User.objects.exclude(username=request.user)
    return render(request, 'usuarios.html', {'users_list': users_list})


@login_required
@permission_required('core.view_persona', raise_exception=True)
def personas(request):
    persons_list = Persona.objects.exclude(tipo_persona=1) # Administrador
    return render(request, 'personas.html', {'persons_list': persons_list})


@login_required
@permission_required('core.view_asamblea', raise_exception=True)
def asambleas(request):
    assemblies_list = Asamblea.objects.exclude(estado=5) # Terminada
    return render(request, 'asambleas.html', {'assemblies_list': assemblies_list})


@login_required
@permission_required('core.view_encuesta', raise_exception=True)
def encuestas(request):
    surveys_list = Encuesta.objects.all()
    return render(request, 'encuestas.html', {'surveys_list': surveys_list})


# GENERAL VIEWS
@login_required
@permission_required(['core.add_users', 'core.add_rel_asamblea_asistente', 'core.add_apartamento'], raise_exception=True)
def home(request):
    return render(request, 'home.html')


@login_required
def usrs_normales(request):
    return render(request, 'main_users_normales.html')