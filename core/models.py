from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Tipo_Documento(models.Model):
    id_tipo_documento = models.BigAutoField(auto_created=True, primary_key=True)
    abreviatura       = models.CharField(max_length=2)
    descripcion       = models.TextField(max_length=21)

    def __str__(self):
        return self.abreviatura

    class Meta:
        verbose_name_plural = 'Tipo De Documento'


class Apartamento(models.Model):
    id_apartamento  = models.BigAutoField(auto_created=True, primary_key=True)
    nro_apartamento = models.IntegerField(validators=[MinValueValidator(101)])
    nro_torre       = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{str(self.nro_torre)} - {self.nro_apartamento}'

    class Meta:
        verbose_name_plural = 'Apartamento'


class Tipo_Persona(models.Model):
    id_tipo_persona = models.BigAutoField(auto_created=True, primary_key=True)
    descripcion     = models.TextField(max_length=21)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Tipo De Persona'


class Persona(models.Model):
    nro_documento       = models.CharField(max_length=10, primary_key=True)
    tipo_documento      = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, related_name='pe_tipo_doc')
    nombres             = models.CharField(max_length=30)
    apellidos           = models.CharField(max_length=30)
    email               = models.EmailField()
    nro_contacto        = models.CharField(max_length=10)
    tipo_persona        = models.ForeignKey(Tipo_Persona, on_delete=models.CASCADE, related_name='pe_tipo_per')
    usuario             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pe_usuario', null=True, blank=True, default=None)
    apartamento         = models.ManyToManyField(Apartamento, related_name='pe_apto', blank=True)
    fecha_registro      = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro Persona')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización Persona')

    def __str__(self):
        if not self.usuario:
            return f'{self.nombres} {self.apellidos}'
        
        return f'{self.nombres} {self.apellidos} - {self.usuario.username}'

    class Meta:
        verbose_name_plural = 'Persona'


class Pregunta(models.Model):
    id_pregunta    = models.BigAutoField(auto_created=True, primary_key=True)
    texto_pregunta = models.TextField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación Pregunta')

    def __str__(self):
        return self.texto_pregunta

    class Meta:
        verbose_name_plural = 'Pregunta'


class Opcion(models.Model):
    id_opcion    = models.BigAutoField(auto_created=True, primary_key=True)
    pregunta     = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='op_pregunta')
    texto_opcion = models.CharField(max_length=100)

    def __str__(self):
        return f'Pregunta: {self.pregunta.id_pregunta} - Opción: {self.id_opcion}'

    class Meta:
        verbose_name_plural = 'Opción'


class Respuesta(models.Model):
    id_respuesta = models.BigAutoField(auto_created=True, primary_key=True)
    usuario      = models.ForeignKey(User, on_delete=models.CASCADE)
    opcion       = models.ForeignKey(Opcion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id_usuario} - {self.id_opcion} - {self.id_pregunta}'

    class Meta:
        verbose_name_plural = 'Respuesta'


class Estado_Encuesta(models.Model):
    id_estado   = models.BigAutoField(auto_created=True, primary_key=True)
    abreviatura = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=10)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Estado Encuesta'


class Encuesta(models.Model):
    id_encuesta    = models.BigAutoField(auto_created=True, primary_key=True)
    titulo         = models.CharField(max_length=150)
    descripcion    = models.TextField(max_length=255)
    pregunta       = models.ManyToManyField(Pregunta, through='Rel_Encuesta_Pregunta', related_name='en_pregunta')
    fecha_inicio   = models.DateField(verbose_name='Fecha Inicio Encuesta', null=True, blank=True, default=None)
    fecha_fin      = models.DateField(verbose_name='Fecha Finalización Encuesta', null=True, blank=True, default=None)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación Encuesta')
    estado         = models.ForeignKey(Estado_Encuesta, on_delete=models.CASCADE, related_name='encu_estado')

    def __str__(self):
        return f'{self.id_encuesta} - {self.titulo}'

    class Meta:
        verbose_name_plural = 'Encuesta'


class Rel_Encuesta_Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.encuesta.id_encuesta} - {self.pregunta.id_pregunta}'
    
    class Meta:
        verbose_name_plural = 'Preguntas De Encuesta'


class Estado_Asamblea(models.Model):
    id_estado   = models.BigAutoField(auto_created=True, primary_key=True)
    abreviatura = models.CharField(max_length=5)
    descripcion = models.CharField(max_length=10)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Estado Asamblea'


class Asamblea(models.Model):
    id_asamblea         = models.BigAutoField(auto_created=True, primary_key=True)
    nombre              = models.CharField(max_length=50)
    lugar_encuentro     = models.CharField(max_length=100)
    fecha_encuentro     = models.DateField(verbose_name='Fecha De Encuentro')
    hora_encuentro      = models.TimeField(verbose_name='Hora De Encuentro')
    usr_admin           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asam_usr_admin')
    encuesta            = models.OneToOneField(Encuesta, on_delete=models.CASCADE, related_name='asam_encuesta', null=True, blank=True, default=None)
    asistente           = models.ManyToManyField(Persona, through='Rel_Asamblea_Asistente', related_name='asam_asistente')
    fecha_creacion      = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación Asamblea')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha actualización Asamblea')
    estado              = models.ForeignKey(Estado_Asamblea, on_delete=models.CASCADE, related_name='asam_estado')

    def __str__(self):
        return f'{self.id_asamblea} - {self.nombre} - {self.usr_admin.username}'

    class Meta:
        verbose_name_plural = 'Asamblea'


class Rel_Asamblea_Asistente(models.Model):
    asamblea  = models.ForeignKey(Asamblea, on_delete=models.CASCADE)
    asistente = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.asamblea.id_asamblea} - {self.asistente.nro_documento}'

    class Meta:
        verbose_name_plural = 'Asistencia Asamblea'