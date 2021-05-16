import json

from django.http import JsonResponse
from rest_framework.views import APIView

from like.models import Like


class LikeView(APIView):
    def post(self, request, *args, **kwargs):
        json_obj = request.body
        json_str = json.loads(json_obj)
        is_up = json_str.get('is_up')  # 字符串 “ture”
        movie_id = json_str.get('movie_id')
        # print(is_up, movie_id, request.user.nickname)
        res = {'code': 200, 'movie_id': movie_id, 'error': None, 'data': {'is_up': is_up}}
        obj = Like.objects.filter(movie_id=movie_id, user=request.user).first()
        if not obj:
            Like.objects.create(is_up=is_up, movie_id=movie_id, user=request.user)
        if obj and obj.is_up == is_up and is_up:
            res['code'] = 40001
            res['error'] = '您已经点赞过了！'
        #     # 取消点赞记录
        #     Like.objects.filter(is_up=is_up, movie_id=movie_id, user=request.user).delete()
        #     res['data']['tips'] = '您已经取消点赞了！'
        if obj and obj.is_up != is_up and not is_up:
            res['code'] = 40002
            res['error'] = '您已经点赞过了！'
        if obj and obj.is_up != is_up and is_up:
            res['code'] = 40003
            res['error'] = '您已经踩过了！'
        if obj and obj.is_up == is_up and not is_up:
            res['code'] = 40004
            res['error'] = '您已经踩过了！'
        #     res['data']['tips'] = '您已经取消踩了！'
        #     # 取消踩记录
        #     Like.objects.filter(is_up=is_up, movie_id=movie_id, user=request.user).delete()
        return JsonResponse(res)


def like_view(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movie_id')
        digg_num = Like.objects.filter(movie_id=movie_id, is_up=True).count()
        bury_num = Like.objects.filter(movie_id=movie_id, is_up=False).count()
        res = {'code': 200, 'movie_id': movie_id, 'data': {'digg_num': digg_num, 'bury_num': bury_num}}
        return JsonResponse(res)
