from urllib.parse import urljoin
import jwt
import requests

from django.conf import settings
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.reverse import reverse
from rest_framework import HTTP_HEADER_ENCODING, authentication

from datamodel import User, Profile


def authenticate_user(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        raise NotAuthenticated()

    url = urljoin(settings.AUTHENTICATE_URL, '/user/profile/')
    response = requests.get(url, headers={'Authorization': request.META['HTTP_AUTHORIZATION']})

    if response.status_code == 401:
        raise AuthenticationFailed()

    data = response.json()
    user = User.init_x_auth_data(data)
    return user


def mock_auth(request):
    if hasattr(settings, 'SWAGGER_URL') and request.path == reverse(settings.SWAGGER_URL):
        return User(email='swagger@swagger.com', company_id=1, profile=Profile(company_id=1), is_authenticated=True,
                    first_name='', last_name='', id=None, is_test=False, has_financial_access=True)
    elif hasattr(settings, 'HEALTH_CHECK_URL') and request.path == reverse(settings.HEALTH_CHECK_URL):
        return User(email='status@swagger.com', company_id=1, profile=Profile(company_id=1), is_authenticated=True,
                    first_name='', last_name='', id=None, is_test=False, has_financial_access=True)
    return


class RemoteUserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        mock_user = mock_auth(request)
        if mock_user:
            return mock_user, None

        user = authenticate_user(request)
        return user, None

    def authenticate_header(self, request):
        # https://github.com/davesque/django-rest-framework-simplejwt
        # The code is copy-pasted of class rest_framework_simplejwt.authentication.JWTAuthentication
        return 'jwt realm="api"'

    def get_header(self, request):
        # https://github.com/davesque/django-rest-framework-simplejwt
        # The code is copy-pasted of class rest_framework_simplejwt.authentication.JWTAuthentication
        header = request.META.get('HTTP_AUTHORIZATION')

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header


class InternalAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        mock_user = mock_auth(request)
        if mock_user:
            return mock_user, None

        x_internal_authorization = request.META.get('HTTP_X_INTERNAL_AUTHORIZATION')
        if x_internal_authorization:
            user_data = jwt.decode(x_internal_authorization, algorithms=['HS256'])
            user = User.init_x_auth_data(user_data)
            return user, None

        return None
