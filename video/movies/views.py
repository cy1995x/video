import random

from django.http import JsonResponse
from django.views import View
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination

from btoken.models import Token
from classification.models import Classification
from comments.models import Comments
from history.models import History
from movies.models import Movies, MoviesDetail, ShortVideo
from utils.my_forms import ReleaseForm
from utils.serializers.pagerSerializers import PagerSerializer


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 5
    ordering = 'rank'
    page_size_query_param = None
    max_page_size = None


class MoviesView(APIView):
    authentication_classes = []

    def get(self, request):
        count = request.GET.get('count')
        if count:
            print('-------top-5------')
            movies = Movies.objects.filter(rank__lte=count)
            ser = PagerSerializer(instance=movies, many=True)
            return JsonResponse(ser.data, safe=False)
        else:
            movies = Movies.objects.filter(rank__lte=100)
            # top100 数据
            print('------get top 100-------')
            # 分页对象
            pg = MyCursorPagination()
            # 分页数据
            pager_movie = pg.paginate_queryset(movies, request=request, view=self)
            # 分页数据序列化
            ser = PagerSerializer(instance=pager_movie, many=True)
            res = pg.get_paginated_response(ser.data)
            return res
    # def get_movies_info(self, movies):
    #     res = {'code': 200, 'error': None, 'data': []}
    #     month_to_eng = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
    #                     '07': 'Jul', '08': 'Aug', '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    #     for movie in movies:
    #         d = dict()
    #         time_list = movie.release_time.strftime('%Y-%m-%d').split('-')
    #         year = time_list[0]
    #         month = month_to_eng[time_list[1]]
    #         day = time_list[2]
    #         d['title'] = movie.title
    #         d['actor'] = movie.actor
    #         d['poster'] = str(movie.poster)
    #         d['year'] = year
    #         d['month'] = month
    #         d['day'] = day
    #         d['score'] = movie.score
    #         d['rank'] = movie.rank
    #         res['data'].append(d)
    #     print(res)
    #     return res


class DetailView(View):

    def get(self, request, m_rank):
        if not Movies.objects.filter(rank=m_rank).first():
            m_rank = 1
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_obj = Token.objects.filter(token=token).first()
        movie_obj = Movies.objects.filter(rank=m_rank).first()
        if token_obj:
            user = token_obj.user
            # 创建历史记录！
            History.objects.update_or_create(user=user, movie=movie_obj, defaults={'user': user, 'movie': movie_obj})
        movie_detail_obj = MoviesDetail.objects.filter(movie=movie_obj).first()
        comment_list = Comments.objects.filter(movie_id=m_rank)
        classification_list = movie_obj.classification_set.all()
        res = self.get_movie_all_info(movie_obj, movie_detail_obj, comment_list, classification_list)
        return JsonResponse(res)

    def get_movie_all_info(self, movie_obj, movie_detail_obj, comment_list, classification_list):
        res = {'code': 200, 'error': None, 'data': {}}
        d = res['data']
        d['poster'] = str(movie_obj.poster)
        d['title'] = movie_obj.title
        d['movie_file'] = str(movie_obj.movie_file)
        d['score'] = movie_obj.score
        d['release_time'] = movie_obj.release_time.strftime('%Y-%m-%d')
        d['release_area'] = movie_detail_obj.release_area
        d['actor'] = movie_obj.actor
        d['upload_user'] = movie_obj.user.nickname
        d['film_length'] = movie_detail_obj.film_length
        d['desc'] = movie_detail_obj.desc
        comments = []
        for comment_obj in comment_list:
            item = dict()
            item['content'] = comment_obj.content
            item['created_time'] = comment_obj.created_time.strftime('%Y-%m-%d %H:%M:%S')
            item['comment_user'] = comment_obj.user.nickname
            item['user_id'] = comment_obj.user.id
            item['pid'] = comment_obj.parent_comment_id
            item['pid_id'] = comment_obj.id
            if comment_obj.parent_comment_id:
                item['pid_username'] = comment_obj.parent_comment.user.nickname
                item['pid_created_time'] = comment_obj.parent_comment.created_time.strftime('%Y-%m-%d %H:%M:%S')
                item['pid_content'] = comment_obj.parent_comment.content
            comments.append(item)
        d['comments'] = comments
        classifications = []
        for classification_obj in classification_list:
            t = dict()
            t['c_id'] = classification_obj.id
            t['classification'] = classification_obj.classification
            classifications.append(t)
        d['classifications'] = classifications
        # print(res)
        return res


class MovieControlView(APIView):
    # 删除视频


    # 视频上传
    def post(self, request):
        print('--------post-release--------')
        res = {'code': 200, 'username': request.user.nickname, 'error': None}
        form = ReleaseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            score = form.cleaned_data['score']
            actor = form.cleaned_data['actor']
            poster = request.FILES.get('poster')
            desc = form.cleaned_data['desc']
            movie_file = request.FILES.get('movie_file')
            # print(title, score, actor, desc, poster, movie_file)
            if poster:
                if movie_file:
                    Movies.objects.create(title=title, score=score, actor=actor, user=request.user,
                                          poster=poster,
                                          movie_file=movie_file)
                else:
                    Movies.objects.create(title=title, score=score, actor=actor, user=request.user,
                                          poster=poster)
            else:
                if movie_file:
                    Movies.objects.create(title=title, score=score, actor=actor, user=request.user,
                                          movie_file=movie_file)
                else:
                    Movies.objects.create(title=title, score=score, actor=actor, user=request.user)
            movie = Movies.objects.filter(title=title, score=score, actor=actor, user=request.user).first()
            # print(movie.rank, movie.title, movie.score)
            # print(movie, movie.rank, movie.title, movie.score)
            MoviesDetail.objects.create(desc=desc, movie=movie)
            cls_obj = Classification.objects.filter(classification='其他').first()
            cls_obj.movie.add(movie)
            res['movie_id'] = movie.rank
        else:
            res['error'] = form.errors
            res['code'] = 60001
        return JsonResponse(res)



# 短视频展示get
def short_video_view(request):
    v_id = request.GET.get('v_id')
    print(v_id)
    if v_id:
        obj = ShortVideo.objects.filter(id=v_id).first()
        video_file = str(obj.video_file)
        res = {'code': 200, 'error': None, 'data': {'video_file': video_file}}
        return JsonResponse(res)
    else:
        video_list = ShortVideo.objects.all()
        random_video_list = random.sample(list(video_list), 8)
        res = {'code': 200, 'error': None, 'data': []}
        for video_obj in random_video_list:
            d = dict()
            d['id'] = video_obj.id
            d['title'] = video_obj.title
            d['poster'] = str(video_obj.poster)
            d['video_file'] = str(video_obj.video_file)
            res['data'].append(d)
        print(res)
        return JsonResponse(res)
