from django.http import JsonResponse

from classification.models import Classification
from movies.models import Movies


def classification_view(request):
    classification_id = request.GET.get('type')
    # 全部电影展示
    if not classification_id:
        res = {'code': 200, 'error': None,'data': []}
        month_to_eng = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                        '07': 'Jul', '08': 'Aug', '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
        movie_obj_list = Movies.objects.all()
        for movie_obj in movie_obj_list:
            c_obj_list = movie_obj.classification_set.all()
            m = []
            for c_obj in c_obj_list:
                m.append(c_obj.classification)
            d = dict()
            d['classifications'] = m
            time_list = movie_obj.release_time.strftime('%Y-%m-%d').split('-')
            year = time_list[0]
            month = month_to_eng[time_list[1]]
            day = time_list[2]
            d['title'] = movie_obj.title
            d['actor'] = movie_obj.actor
            d['poster'] = str(movie_obj.poster)
            d['year'] = year
            d['month'] = month
            d['day'] = day
            d['score'] = movie_obj.score
            d['rank'] = movie_obj.rank
            res['data'].append(d)
        print(res)
        return JsonResponse(res)
    # print(classification_id)
    # 按照类型展示
    else:
        c_obj = Classification.objects.filter(id=classification_id).first()
        movie_obj_list = c_obj.movie.all()
        # print(c_obj, movie_obj_list)
        res = {'code': 200, 'error': None, 'type': c_obj.classification, 'data': []}
        month_to_eng = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                        '07': 'Jul', '08': 'Aug', '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
        for movie_obj in movie_obj_list:
            d = dict()
            time_list = movie_obj.release_time.strftime('%Y-%m-%d').split('-')
            year = time_list[0]
            month = month_to_eng[time_list[1]]
            day = time_list[2]
            d['title'] = movie_obj.title
            d['actor'] = movie_obj.actor
            d['poster'] = str(movie_obj.poster)
            d['year'] = year
            d['month'] = month
            d['day'] = day
            d['score'] = movie_obj.score
            d['rank'] = movie_obj.rank
            m = []
            for classification_obj in movie_obj.classification_set.all():
                m.append(classification_obj.classification)
            d['classifications'] = m
            res['data'].append(d)
        # print(res)
        return JsonResponse(res)
