from btoken.models import Token
from rest_framework.request import exceptions
from rest_framework.authentication import BaseAuthentication


class Authentication(BaseAuthentication):
    """登陆认证类"""

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败！')
        return token_obj.user, token_obj

