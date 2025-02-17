from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateApartamento, CreatePersona, CreateAsamblea, UpdateUsuario, UpdatePersona, UpdateAsamblea
from .models import Persona, Asamblea, Estado_Asamblea

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

    if request.method == 'POST':
        try:
            form_asamblea = UpdateAsamblea(request.POST, instance=asamblea)
            form_asamblea.save()
            return redirect('asambleas')
        except:
            return render(request, 'update_asambleas.html', {
                'asamblea': asamblea,
                'form_asamblea': form_asamblea,
                'error': 'No se pudo editar la información de la asamblea.'
            })

    form_asamblea = UpdateAsamblea(instance=asamblea)
    return render(request, 'update_asambleas.html', {
        'asamblea': asamblea,
        'form_asamblea': form_asamblea
    })


# CONSULTATION VIEWS
def usuarios(request):
    users_list = User.objects.exclude(username=request.user)
    return render(request, 'usuarios.html', {'users_list': users_list})


@login_required
@permission_required('core.view_persona', raise_exception=True)
def personas(request):
    persons_list = Persona.objects.exclude(tipo_persona=1)
    return render(request, 'personas.html', {'persons_list': persons_list})


@login_required
@permission_required('core.view_asamblea', raise_exception=True)
def asambleas(request):
    assemblies_list = Asamblea.objects.all()
    return render(request, 'asambleas.html', {'assemblies_list': assemblies_list})


# GENERAL VIEWS
@login_required
@permission_required(['core.add_users', 'core.add_rel_asamblea_asistente', 'core.add_apartamento'], raise_exception=True)
def home(request):
    return render(request, 'home.html')


@login_required
#@permission_required('core.view_encuesta', raise_exception=True)
def encuestas(request):
    return render(request, 'encuestas.html')


@login_required
def usrs_normales(request):
    return render(request, 'main_users_normales.html')