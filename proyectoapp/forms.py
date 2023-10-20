from django import forms
from allauth.account.forms import SignupForm
from .models import Formulario, User

class CustomSignupForm(SignupForm):
    birthday = forms.DateField(label='Birthday', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.birthday = self.cleaned_data['birthday']
        user.save()
        return user

class SolicitarForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = [
            'email',
            'encargado',
            'motivo',
            'jornada',
            'fecha',
            'hora_ingreso',
            'hora_regreso',
        ]

        