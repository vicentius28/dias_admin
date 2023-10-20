from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.models import SocialLogin, SocialAccount, SocialApp
from django.contrib.auth import get_user_model
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

class CustomGoogleOAuth2Adapter(OAuth2Adapter):
    provider_id = GoogleProvider.id

    def complete_login(self, request, app, token, response):
        if 'access_type' in app.extra_data and 'offline' in app.extra_data['access_type']:
            token.token = app.extra_data['access_token']
            token.token_secret = None
        else:
            token.token = app.extra_data['access_token']
            token.token_secret = None
        return self.get_provider().sociallogin_from_response(request, response)

provider_classes = [CustomGoogleOAuth2Adapter]

class CustomGoogleProvider(OAuth2Provider):
    id = GoogleProvider.id
    package = GoogleProvider.package

    def get_app(self):
        app = SocialApp.objects.get(provider=GoogleProvider.id)
        if app:
            app.extra_data = app.extra_data or {}
        return app

    def get_auth_params(self, request, action):
        params = super().get_auth_params(request, action)
        app = self.get_app()
        access_type = app.extra_data.get('access_type')
        prompt = app.extra_data.get('prompt')
        if access_type:
            params['access_type'] = access_type
        if prompt:
            params['prompt'] = prompt
        return params

    def format_email(self, response):
        return response.get('email')

provider_classes = [CustomGoogleProvider]

class GoogleLogin:
    def login_and_associate(self, user, extra_data):
        user.username = extra_data.get('username') or user.username
        user.email = extra_data.get('email') or user.email
        user.save()

    def login_and_create(self, extra_data):
        User = get_user_model()
        user = User(username=extra_data.get('username'), email=extra_data.get('email'))
        user.save()
        return user
