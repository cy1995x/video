from rest_framework import serializers


class PagerSerializer(serializers.Serializer):
    title = serializers.CharField()
    actor = serializers.CharField()
    poster = serializers.ImageField()
    score = serializers.CharField()
    rank = serializers.IntegerField()
    release_time = serializers.SerializerMethodField()

    def get_release_time(self, obj):
        month_to_eng = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
                        '07': 'Jul', '08': 'Aug', '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
        time_list = obj.release_time.strftime('%Y-%m-%d').split('-')
        year = time_list[0]
        month = month_to_eng[time_list[1]]
        day = time_list[2]
        return {'year': year, 'month': month, 'day': day}

