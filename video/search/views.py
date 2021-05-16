from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Users
from utils.serializers.userSerializers import UserSerializer


# 用户搜索
class SearchUserView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        keyword = request.GET.get('keyword')
        # print(user, keyword)
        if not keyword:
            return JsonResponse([],safe=False)
        query_user = Users.objects.filter(nickname__contains=keyword)
        res = UserSerializer(instance=query_user, many=True)
        print(res.data)
        return Response(res.data)
