from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SolicitarForm
from .models import User,Formulario
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.db import connection
# Create your views here.
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from django.conf import settings
#email
from django.core.mail import send_mail
import logging

class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

@login_required
def index(request):
    context={}
    return render(request, 'proyectoapp/index.html',context)
def profile(request):
    return render(request, 'account/profile.html')
def revisar(request):
    return render(request, 'proyectoapp/revisar.html')


#Listado de Usuarios
def Listado(request):
    usuario_logeado = request.user.email
    formListados = Formulario.objects.all().filter(encargado=usuario_logeado, estado=2).order_by('created_at' )
    return render (request, "proyectoapp/ListadoFormulario.html", {"formularios":formListados})

from django.db import connection

#listado del Historial
def historial(request):
    usuario = request.user
    cursor = connection.cursor()
    cursor.execute("SELECT group_id FROM proyectoapp_user_groups WHERE user_id = %s", [usuario.id])
    group_id = cursor.fetchone()[0]  # Obtiene el primer valor de la consulta
    if group_id in [10, 4]:  # Verifica si group_id está en la lista [1, 2, 4]
        formListados = Formulario.objects.filter(group_id=group_id).order_by('created_at')
    elif group_id in [11]:
        formListados = Formulario.objects.order_by('created_at')
    else:
        pass
        

    return render(request, "proyectoapp/historial.html", {"formularios": formListados})


def usuarios(request):
    usuario = request.user
    cursor = connection.cursor()
    cursor.execute("SELECT group_id FROM proyectoapp_user_groups WHERE user_id = %s", [usuario.id])
    group_id = cursor.fetchone()[0]  # Obtiene el primer valor de la consulta
    if group_id in [10, 4]:  # Verifica si group_id está en la lista [1, 2, 4]
        userListados = User.objects.filter(grupo_encargado_id=group_id).order_by('email')
    elif group_id in [11]:
        userListados = User.objects.order_by('email')
    else:
        pass
        
    return render(request, "proyectoapp/usuarios.html", {"usuarios": userListados})



def aceptar_formulario(request, formulario_id):
    if request.method == 'POST':
        logger = logging.getLogger(__name__)
        try:
            formulario = Formulario.objects.get(id=formulario_id)
            formulario.estado = 1  # Cambiar el estado a 1 (aceptado)
            formulario.save()
            fecha = Formulario.objects.filter(id=formulario_id).get().fecha.strftime('%d/%m/%Y')
            subject = 'Estado Solicitud'
            message = 'tu solicitud para el día {} fue aceptada'.format(fecha)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [Formulario.objects.filter(id=formulario_id).get().email]

            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, "correo enviado con éxito.")
        except Exception as e:
            logger.error('Error al enviar correo: %s', str(e))
            # Manejar el caso en el que el formulario no existe
    return HttpResponseRedirect(reverse('Listado')) 

def denegar_formulario(request, formulario_id):
    if request.method == 'POST':
        logger = logging.getLogger(__name__)
        try:
            formulario = Formulario.objects.get(id=formulario_id)
            formulario.estado = 0  # Cambiar el estado a 0 (denegado)
            formulario.save()
            fecha = Formulario.objects.filter(id=formulario_id).get().fecha.strftime('%d/%m/%Y')
            subject = 'Estado Solicitud'
            message = 'tu solicitud para el día {} fue Denegada'.format(fecha)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [Formulario.objects.filter(id=formulario_id).get().email]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, "correo enviado con éxito.")
        except Exception as e:
            logger.error('Error al enviar correo: %s', str(e))

    return HttpResponseRedirect(reverse('Listado')) 
    

   



def formulario(request):
    if request.method == 'POST':
        form = SolicitarForm(request.POST)
        if form.is_valid():
            user = request.user
            solicitud = form.save(commit=False)
            solicitud.user = user
            
            if user.dias_tomados <= 1 and solicitud.jornada == 1 and solicitud.motivo == 1:
                user.dias_tomados += 1
                user.dias_restantes -= 1
            elif user.dias_tomados <= 1.5 and solicitud.jornada == 0.5:
                user.dias_tomados += 0.5
                user.dias_restantes -= 0.5
            elif user.dias_tomados <= 1.75 and solicitud.jornada == 0.25:
                user.dias_tomados += 0.25
                user.dias_restantes -= 0.25
            elif user.dias_cumpleaños == 1 and solicitud.motivo == 0:
                user.dias_cumpleaños -= 1
            else:
                messages.error(request, "No tiene Días disponibles.")
                return render(request, 'proyectoapp/formulario.html')
            
            user.save()
            solicitud.save()

            #enviar email
            logger = logging.getLogger(__name__)
            try:
                subject = 'Nueva solicitud recibida'
                message = 'revisar solicitud en el siguiente link de días administrativos http://127.0.0.1:8000/ListadoFormulario/'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get("encargado"),]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request, "correo enviado con éxito.")
            except Exception as e:
                logger.error('Error al enviar correo: %s', str(e))
            #email

            
            
            messages.success(request, "Formulario enviado con éxito.")
            return render(request, 'proyectoapp/index.html')
        else:
            messages.error(request, "El formulario no es válido. Por favor, corrige los errores.")
    else:
        form = SolicitarForm()
    
    return render(request, 'proyectoapp/formulario.html', {'form': form})



def get (self,request,*args,**kwargs):
    if request.user.is_authenticated:
        return render(self.template_name)
    else:
        return redirect('login')




@receiver(post_save, sender=Formulario)
def restar_dias_restantes(sender, instance, **kwargs):
    if instance.estado == 0 or instance.estado == 4 :
        email_del_formulario = instance.email
        try:
            user = User.objects.get(email=email_del_formulario)
            if user.dias_restantes >= 0 and user.dias_restantes <=1 and instance.jornada == 1 and instance.motivo == 1:
                user.dias_tomados -=1
                user.dias_restantes += 1
            elif user.dias_restantes >= 0 and user.dias_restantes <=1.5 and instance.jornada == 0.5:
                user.dias_tomados -=0.5
                user.dias_restantes += 0.5
            elif user.dias_restantes >= 0 and user.dias_restantes <=1.75 and instance.jornada == 0.25:
                user.dias_tomados -=0.25
                user.dias_restantes += 0.25
            elif user.dias_cumpleaños == 0 and instance.motivo == 0:
                user.dias_cumpleaños += 1
            user.save()
        except User.DoesNotExist:
            pass



#proteccion url








    


    
