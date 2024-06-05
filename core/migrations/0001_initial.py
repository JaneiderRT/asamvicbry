# Generated by Django 5.0.4 on 2024-05-16 00:57

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartamento',
            fields=[
                ('id_apartamento', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nro_apartamento', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('nro_torre', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'Apartamento',
            },
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id_encuesta', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creacion Encuesta')),
                ('estado', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Encuesta',
            },
        ),
        migrations.CreateModel(
            name='Estado_Asamblea',
            fields=[
                ('id_estado', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('abreviatura', models.CharField(max_length=5)),
                ('descripcion', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Estado Asamblea',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id_pregunta', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('texto_pregunta', models.TextField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creacion Pregunta')),
            ],
            options={
                'verbose_name_plural': 'Pregunta',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Documento',
            fields=[
                ('id_tipo_documento', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('abreviatura', models.CharField(max_length=2)),
                ('descripcion', models.TextField(max_length=21)),
            ],
            options={
                'verbose_name_plural': 'Tipo De Documento',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Persona',
            fields=[
                ('id_tipo_persona', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('descripcion', models.TextField(max_length=21)),
            ],
            options={
                'verbose_name_plural': 'Tipo De Persona',
            },
        ),
        migrations.CreateModel(
            name='Asamblea',
            fields=[
                ('id_asamblea', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('lugar_encuentro', models.CharField(max_length=100)),
                ('fecha_encuentro', models.DateField(verbose_name='Fecha De Encuentro')),
                ('hora_encuentro', models.TimeField(verbose_name='Hora De Encuentro')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creacion Asamblea')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion Asamblea')),
                ('usr_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asam_usr_admin', to=settings.AUTH_USER_MODEL)),
                ('encuesta', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asam_encuesta', to='core.encuesta')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asam_estado', to='core.estado_asamblea')),
            ],
            options={
                'verbose_name_plural': 'Asamblea',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('nro_documento', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('nro_contacto', models.CharField(max_length=10)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro Persona')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha Actualizacion Persona')),
                ('apartamento', models.ManyToManyField(blank=True, default=None, related_name='pe_apto', to='core.apartamento')),
                ('usuario', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pe_usuario', to=settings.AUTH_USER_MODEL)),
                ('tipo_documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pe_tipo_doc', to='core.tipo_documento')),
                ('tipo_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pe_tipo_per', to='core.tipo_persona')),
            ],
            options={
                'verbose_name_plural': 'Persona',
            },
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id_opcion', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('texto_opcion', models.CharField(max_length=100)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='op_pregunta', to='core.pregunta')),
            ],
            options={
                'verbose_name_plural': 'Opcion',
            },
        ),
        migrations.AddField(
            model_name='encuesta',
            name='pregunta',
            field=models.ManyToManyField(related_name='en_pregunta', to='core.pregunta'),
        ),
        migrations.CreateModel(
            name='Rel_Asamblea_Asistente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asamblea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.asamblea')),
                ('asistente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.persona')),
            ],
            options={
                'verbose_name_plural': 'Asistencia Asamblea',
            },
        ),
        migrations.AddField(
            model_name='asamblea',
            name='asistente',
            field=models.ManyToManyField(related_name='asam_asistente', through='core.Rel_Asamblea_Asistente', to='core.persona'),
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id_respuesta', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.opcion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Respuesta',
            },
        ),
    ]
