import json


from django.http import JsonResponse
from rest_framework.views import APIView

from btoken.models import Token
from users.models import Users
from utils.md5 import md5_token, md5_pwd


class TokenView(APIView):
    # 用户登陆
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # print(request.user)
        # print(request.auth)
        json_obj = json.loads(request.body)
        name = json_obj.get('username')
        pwd = json_obj.get('password')
        res = {'username': name, 'code': 200, 'data': {}}
        m_pwd = md5_pwd(pwd)
        print(name, m_pwd)
        try:
            user = Users.objects.filter(nickname=name, password=m_pwd).first()
            if not user:
                res['code'] = 1001
                res['error'] = '用户名或密码错误！'
            token = md5_token(name)
            Token.objects.update_or_create(user=user, defaults={'token': token})
            res['data']['token'] = token
        except Exception as e:
            pass
        print(res)
        return JsonResponse(res)
