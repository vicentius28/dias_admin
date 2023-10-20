from django.contrib import admin
from .models import User,Formulario
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.site_header = 'CLSB Administrador'
admin.site.index_title = 'Pestañas'
admin.site.site_title = 'CSLB Administrador'

class FormResources (resources.ModelResource):
    fields = (
            'email',
            'encargado',
            'motivo',
            'jornada',
            'fecha',
            'hora_ingreso',
            'hora_regreso',
            'created_at',
            'estado',
    )
    class Meta:
        model = Formulario

class Formularioadmin(ImportExportModelAdmin):
    resource_class = FormResources
    admin.site.site_header = 'Formulario'
    admin.site.index_title = 'Pestañas'
    admin.site.site_title = 'Formulario'
    list_display = ('email','encargado','fecha','created_at','estado')
    def estado(self, obj):
        if obj.estado == 1:
            return "Aprobado"
        elif obj.estado == 0:
            return "Denegado"
        else:
            return "Pendiente"
        
    search_fields = ('email', 'created_at','estado')
    date_hierarchy = 'created_at'

class UserResources (resources.ModelResource):
    fields = (
            'groups',
            'email',
            'jefe',
            'birthday',
            'date_joined',
            'dias_tomados',
            'dias_restantes',
            'dias_cumpleaños',
    )
    class Meta:
        model = User

class Useradmin(ImportExportModelAdmin):
    resource_class = UserResources
    admin.site.site_header = 'Usuario'
    admin.site.index_title = 'Pestañas'
    admin.site.site_title = 'Usuario'
    list_display = ('email','jefe','date_joined','dias_restantes','dias_cumpleaños')
    def estado(self, obj):
        if obj.estado == 1:
            return "Aprobado"
        elif obj.estado == 0:
            return "Denegado"
        else:
            return "Pendiente"
        
    search_fields = ('email', 'dias_restantes','dias_cumpleaños')
    date_hierarchy = 'date_joined'

admin.site.register(Formulario,Formularioadmin)
admin.site.register(User,Useradmin)
