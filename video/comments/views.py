import json

from django.http import JsonResponse
from rest_framework.views import APIView

from comments.models import Comments


class CommentsView(APIView):
    def post(self, request, *args, **kwargs):
        json_obj = request.body
        json_str = json.loads(json_obj)
        print(json_str)
        movie_id = json_str.get('movie_id')
        content = json_str.get('content')
        res = dict()
        if not content:
            res['code'] = 50001
            res['error'] = "评论不能为空！"
            return JsonResponse(res)
        pid = json_str.get('pid')
        if pid:
            content = content.split('\n')[1]
        user = request.user
        comment_obj = Comments.objects.create(content=content,
                                              parent_comment_id=pid,
                                              user=user, movie_id=movie_id)
        res['code'] = 200
        res['data'] = {'created_time': comment_obj.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'username': comment_obj.user.nickname,
                       'content': content}
        return JsonResponse(res)
