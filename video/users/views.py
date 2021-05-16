import json
from datetime import date

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views import View
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from btoken.models import Token
from users.models import Users, U2U
from users.tasks import send_sms
from utils.md5 import md5_pwd, md5_token
from utils.random_code import get_random_code


# 注册
class UserView(View):

    def post(self, request, *args, **kwargs):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        phone = json_obj.get('phone')
        sms_num = json_obj.get('sms_num')
        res = {'username': username, 'code': 200, 'data': {}}
        if password_1 != password_2:
            res['code'] = 10002
            res['error'] = '两次密码不一致！'
            return JsonResponse(res)
        cache_key = 'sms_%s' % phone
        code = cache.get(cache_key)
        if not code:
            res['code'] = 10003
            res['error'] = '请点击免费获取验证码！'
            return JsonResponse(res)
        if str(code) != sms_num:
            res['code'] = 10004
            res['error'] = '验证码输入有误！'
            return JsonResponse(res)
        old_user = Users.objects.filter(nickname=username).first()
        if old_user:
            res['code'] = 10005
            res['error'] = '该用户名已被注册！'
            return JsonResponse(res)
        # 密码加密
        m_pwd = md5_pwd(password_1)
        try:
            user = Users.objects.create(nickname=username, password=m_pwd, phone=phone)
        except Exception as e:
            res['code'] = 10005
            res['error'] = '该用户名已被注册！%s' % e
            return JsonResponse(res)
        token = md5_token(username)
        Token.objects.update_or_create(user=user, defaults={'token': token})
        res['data']['token'] = token
        return JsonResponse(res)


# 我的信息
class UserInfoView(APIView):

    def get(self, request, username):
        if request.GET.get('logout'):
            print('-------get-logout-----')
            res = {'code': 200}
            try:
                request.auth.delete()
                res['username'] = request.user.nickname
            except Exception as e:
                res['error'] = e
            return JsonResponse(res)
        else:
            print('-------get_display------', )
            user = request.user
            # 粉丝,关注数
            fans_count = U2U.objects.filter(user=user).count()
            attention_account = U2U.objects.filter(fans=user).count()
            res = {
                'code': 200,
                'data': {
                    'username': user.nickname,
                    'email': user.email,
                    'password': user.password,
                    'phone': user.phone,
                    'sign': user.sign,
                    'gender': user.gender,
                    'avatar': str(user.avatar),
                    'fans_count': fans_count,
                    'attention_account': attention_account,
                }
            }
            # print(res)
            return JsonResponse(res)

    # 修改信息的视图函数(put请求)
    def post(self, request, username):
        json_str = request.body
        json_obj = json.loads(json_str)
        print('------put-update------')
        nickname = json_obj.get('username')
        if request.user.nickname != nickname:
            older_user = Users.objects.filter(nickname=nickname).first()
        else:
            older_user = None
        res = {'username': request.user.nickname, 'code': 200, 'error': None, 'data': {}}
        if older_user:
            res['code'] = 20001
            res['error'] = '该用户名已被注册！'
            return JsonResponse(res)
        phone = json_obj.get('phone')
        email = json_obj.get('email')
        sign = json_obj.get('sign')
        gender = int(json_obj.get('gender'))
        password = json_obj.get('password')
        if password == request.user.password:
            m_pwd = password
        else:
            m_pwd = md5_pwd(password)
        token = md5_token(nickname)
        Users.objects.filter(nickname=request.user.nickname).update(
            nickname=nickname,
            password=m_pwd,
            phone=phone,
            email=email,
            sign=sign,
            gender=gender
        )
        new_user = Users.objects.get(nickname=nickname)
        Token.objects.filter(user=request.user).update(
            user=new_user,
            token=token
        )
        res['username'] = nickname
        res['data']['token'] = token
        return HttpResponse(json.dumps(res))


# 验证码路由函数
def sms_view(request):
    print('------sms-------')
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj.get('phone')
    # 获取六位随机验证码
    code = get_random_code(6)
    cache_key = 'sms_%s' % phone
    cache.set(cache_key, code, 60)
    # 异步提交发送短信任务
    # print(code, phone)
    res = send_sms.delay(phone, code)
    return JsonResponse({'code': 200})


# 图像视图
class AvatarView(APIView):
    def post(self, request, username):
        user = request.user
        res = {'username': user.nickname, 'code': 200, 'error': None}
        try:
            avatar = request.FILES['avatar']
            # print(avatar.name)
            user.avatar = avatar
            user.save()
        except Exception as e:
            res['code'] = 30001
            res['error'] = '请选择图像！'
        return JsonResponse(res)


# 粉丝视图
class FansView(APIView):
    def get(self, request, username):
        user = request.user
        u2u_obj = U2U.objects.filter(user=user)
        res = self.get_fans_info(user, u2u_obj)
        # print(res)
        return JsonResponse(res)

    def post(self, request, username):
        user = request.user
        name = request.POST.get('name')
        fans = Users.objects.filter(nickname=name).first()
        U2U.objects.update_or_create(user=fans, fans=user, defaults={'user': fans, 'fans': user})
        return JsonResponse({'code': 200})

    @staticmethod
    def get_fans_info(user, u2u_obj):
        res = {'avatar': str(user.avatar), 'code': 200, 'count': len(u2u_obj), 'data': []}
        for obj in u2u_obj:
            fans_obj = obj.fans
            d = dict()
            d['username'] = fans_obj.nickname
            d['avatar'] = str(fans_obj.avatar)
            d['email'] = fans_obj.email
            d['time'] = (date.today() - obj.created_time).days
            if U2U.objects.filter(user=fans_obj, fans=user):
                d['is_focus_each_other'] = True
            else:
                d['is_focus_each_other'] = False
            res['data'].append(d)
        return res


# 关注视图
class AttentionView(APIView):
    def get(self, request, username):
        user = request.user
        u2u_obj = U2U.objects.filter(fans=user)
        res = self.get_attention_info(user, u2u_obj)
        # print(res)
        return JsonResponse(res)

    # 取关
    def post(self, request, username):
        name = request.POST.get('name')
        user = Users.objects.filter(nickname=name).first()
        U2U.objects.filter(user=user, fans=request.user).delete()
        return JsonResponse({'code': 200})

    @staticmethod
    def get_attention_info(user, u2u_obj):
        res = {'avatar': str(user.avatar), 'code': 200, 'count': len(u2u_obj), 'data': []}
        for obj in u2u_obj:
            user_obj = obj.user
            d = dict()
            d['username'] = user_obj.nickname
            d['avatar'] = str(user_obj.avatar)
            d['email'] = user_obj.email
            d['time'] = obj.created_time.strftime('%Y-%m-%d')
            res['data'].append(d)
        return res


# 个人空间
def space_view(request, username):
    print('-------space-------')
    res = {'username': username, 'is_fans': False, 'code': 200, 'data': {}}
    name = request.GET.get('username')
    try:
        user = Users.objects.filter(nickname=username).first()
        print(user)
        name = Users.objects.filter(nickname=name).first()
        res['data']['avatar'] = str(user.avatar)
        res['data']['username'] = user.nickname
        res['data']['gender'] = user.get_gender_display()
        res['data']['email'] = user.email
        res['data']['sign'] = user.sign
        res['data']['fans_count'] = user.fans.all().count()
        res['data']['attention_count'] = user.user.all().count()
        u2u_obj = U2U.objects.filter(fans=name, user=user).first()
        movie_list = user.movies_set.all()
        print(movie_list)
        movie_info = []
        for movie_obj in movie_list:
            movie_info.append((movie_obj.rank, movie_obj.title, movie_obj.release_time.strftime('%Y-%m-%d')))
        res['data']['movies'] = movie_info
        if u2u_obj:
            res['is_fans'] = True
    except Exception as e:
        res['code'] = 60001
    print(res)
    return JsonResponse(res)


# ta的关注
class AttentionInfoView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        print(username)
        try:
            user = Users.objects.filter(nickname=username).first()
            u2u_obj = U2U.objects.filter(user=user).all()
            res = self.get_attention_info(user, u2u_obj)
            print(res)
            return JsonResponse(res)
        except:
            return JsonResponse({'code': 70001, 'error': '没有该用户!'})

    @staticmethod
    def get_attention_info(user, u2u_obj):
        res = {'avatar': str(user.avatar), 'code': 200, 'count': len(u2u_obj), 'data': []}
        for obj in u2u_obj:
            user_obj = obj.fans
            d = dict()
            d['username'] = user_obj.nickname
            d['avatar'] = str(user_obj.avatar)
            d['email'] = user_obj.email
            res['data'].append(d)
        print(res)
        return res


class FansInfoView(APIView):
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        login_user = request.user
        username = kwargs.get('username')
        print(username)
        try:
            user = Users.objects.filter(nickname=username).first()
            u2u_obj = U2U.objects.filter(fans=user).all()
            res = self.get_attention_info(user, u2u_obj,login_user)

            return JsonResponse(res)
        except:
            return JsonResponse({'code': 70001, 'error': '没有该用户!'})

    @staticmethod
    def get_attention_info(user, u2u_obj,login_user):
        res = {'avatar': str(user.avatar), 'code': 200, 'count': len(u2u_obj), 'data': []}
        for obj in u2u_obj:
            user_obj = obj.user
            d = dict()
            d['username'] = user_obj.nickname
            d['avatar'] = str(user_obj.avatar)
            d['email'] = user_obj.email
            res['data'].append(d)
            if U2U.objects.filter(user=user_obj, fans=login_user):
                d['is_focus_each_other'] = True
            else:
                d['is_focus_each_other'] = False
        print(res)
        return res
