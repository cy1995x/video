from .models import History
from rest_framework.views import APIView
from users.models import Users
from django.http import JsonResponse
import json


class HistoryView(APIView):
    def get(self, request):
        # print(request.user)
        res = self.get_all_historys(request.user)
        # print(res)
        return JsonResponse(res)

    def get_all_historys(self, user):
        res = {'code': 200, 'error': None, 'avatar': str(user.avatar)}

        history_list = []
        historys = History.objects.filter(user_id=user.id).order_by('-time')
        for history in historys:
            item = dict()
            item['rank'] = history.movie.rank
            item['id'] = history.id
            item['nickname'] = history.user.nickname
            item['movie'] = history.movie.title
            item['time'] = history.time.strftime('%Y-%m-%d %H:%M:%S')
            history_list.append(item)
        res['data'] = history_list
        return res

    def post(self, request):
        json_obj = request.body
        json_str = json.loads(json_obj)
        mid = json_str['movie_id']
        try:
            h = History.objects.get(id=mid)
        except:
            res = {'code': 11201, 'error': '创建历史记录失败'}
            return JsonResponse(res)
        h.delete()
        res = {'code': 200, 'error': None}
        return JsonResponse(res)
