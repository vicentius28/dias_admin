from allauth.account.signals import user_logged_in
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

@receiver(user_logged_in)
def associate_google_account_with_existing_user(sender, request, user, **kwargs):
    # Comprueba si el usuario ha iniciado sesión a través de una cuenta de Google
    sociallogin = kwargs.get('sociallogin')
    if sociallogin and sociallogin.account.provider == 'google':
        # Obtiene el correo electrónico asociado con la cuenta de Google
        google_email = sociallogin.account.extra_data.get('email')
        # Comprueba si existe un usuario con el mismo correo electrónico en la base de datos
        User = get_user_model()
        existing_user = User.objects.filter(email=google_email).first()
        if existing_user:
            # Asocia la cuenta de Google con el usuario existente
            sociallogin.connect(request, sociallogin.account)
