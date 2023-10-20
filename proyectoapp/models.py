from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db import connection
from allauth.socialaccount.models import SocialAccount,SocialApp
from django.contrib.auth import login

class User(AbstractUser):
    password = models.CharField(max_length=100, verbose_name='contraseña', default="1320")
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    jefe = models.EmailField('correo jefe', max_length=254)
    jefe_id = models.IntegerField(default=None, null=True, blank=True)
    grupo_encargado_id = models.IntegerField(default=None, null=True, blank=True)  # Campo para almacenar group_id
    is_superuser = models.BooleanField(default=False)
    birthday = models.DateField('Cumpleaños',blank=True, null=True)
    date_joined = models.DateTimeField('Fecha Ingreso', default=timezone.now)
    dias_tomados = models.FloatField(default=0, verbose_name='Días Tomados')
    dias_restantes = models.FloatField(default=2, verbose_name='Días Restantes')
    dias_cumpleaños = models.FloatField(default=1, verbose_name='Días cumpleaños')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
         # Dividir el email en partes
        parts = self.email.split('@')[0].split('.')
        if len(parts) >= 2:
            self.first_name = parts[0]
            self.last_name = parts[1]
            self.username = f"{self.first_name} {self.last_name}"

        # Obtener el group_id basado en el email del encargado
        try:
            encargado_email = User.objects.get(email=self.jefe)
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM proyectoapp_user_groups WHERE user_id = %s", [encargado_email.id])
            self.jefe_id = cursor.fetchone()[0]  # Obtiene el primer valor de la consulta
            self.encargado_id = self.jefe_id
            cursor.execute("SELECT group_id FROM proyectoapp_user_groups WHERE user_id = %s", [self.jefe_id])
            self.grupo_encargado_id = cursor.fetchone()[0]
        except User.DoesNotExist:
            self.grupo_encargado_id = None  # Opcional: Manejo en caso de que no se encuentre el usuario
        super(User, self).save(*args, **kwargs)






# Create your models here.
options = [
    [0,'Denegado'],
    [1,'Aprobado'],
    [2,'pendiente'],
    [3,'Tomado'],
    [4,'No Tomado']
]

    #opciones
options_mot = [
    [0,'Dia De Cumpleaños'],
    [1,'Dia Administrativo'],
]
options_jor = [
    [1,'Jornada Completa'],
    [0.5,'1/2 Jornada'],
    [0.25,'1/4 Jornada']
]

class Formulario(models.Model):
    email = models.EmailField()
    encargado = models.EmailField(default='Sin encargado')
    motivo = models.IntegerField(choices=options_mot, default='Dia Administrativo')
    jornada = models.FloatField(choices=options_jor, default='Jornada Completa')
    fecha = models.DateField()
    hora_ingreso = models.TimeField()
    hora_regreso = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    estado = models.IntegerField(choices=options, default=2)
    group_id = models.IntegerField(default=None, null=True, blank=True)  # Campo para almacenar group_id
    encargado_id = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Obtener el group_id basado en el email del encargado
        try:
            encargado_email = User.objects.get(email=self.encargado)
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM proyectoapp_user_groups WHERE user_id = %s", [encargado_email.id])
            encargado_id = cursor.fetchone()[0]  # Obtiene el primer valor de la consulta
            self.encargado_id = encargado_id
            cursor.execute("SELECT group_id FROM proyectoapp_user_groups WHERE user_id = %s", [self.encargado_id])
            self.group_id = cursor.fetchone()[0]
        except User.DoesNotExist:
            self.group_id = None  # Opcional: Manejo en caso de que no se encuentre el usuario
        super(Formulario, self).save(*args, **kwargs)


    
    