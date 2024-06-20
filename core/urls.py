from django.urls import path

from . import views

urlpatterns = [
    # AUTHENTICATION PATHS
    path('', views.index, name='index'),
    path('singout/', views.singout, name='singout'),

    # USERS PATHS
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/create/', views.create_users, name='create_users'),
    path('usuarios/update/<int:user_id>', views.update_users, name='update_users'),

    # PERSONS PATHS
    path('personas/', views.personas, name='personas'),
    path('personas/create/', views.create_personas, name='create_personas'),
    path('personas/update/<int:persona_id>/', views.update_personas, name='update_personas'),

    # APARTAMENTS PATHS
    #path('apartamentos/', views.apartamentos, name='apartamentos'),
    path('home/apartamentos/create/', views.create_apartamentos, name='create_apartamentos'),
    #path('apartamentos/update/<int:apartamentos_id>', views.update_apartamentos, name='update_apartamentos'),

    #ASAMBLEAS PATHS
    path('asambleas/', views.asambleas, name='asambleas'),
    path('asambleas/create/', views.create_asambleas, name='create_asambleas'),
    path('asambleas/update/<int:asamblea_id>', views.update_asambleas, name='update_asambleas'),

    # POLLS PATHS
    path('encuestas/', views.encuestas, name='encuestas'),
    path('encuestas/create/', views.create_encuestas, name='create_encuestas'),
    path('encuestas/update/<int:encuesta_id>', views.update_encuestas, name='update_encuestas'),

    # QUESTIONS PATHS
    path('encuestas/preguntas/', views.preguntas, name='preguntas'),
    path('encuestas/preguntas/create/', views.create_preguntas, name='create_preguntas'),

    # GENERAL PATHS
    path('home/', views.home, name='home'),
    path('usuarios-normales/', views.usrs_normales, name='usrs_normales'),
]