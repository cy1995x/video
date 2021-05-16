from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    gender = serializers.CharField(source='get_gender_display')
    avatar = serializers.ImageField()
    id = serializers.IntegerField()
    fans_count = serializers.SerializerMethodField()

    def get_fans_count(self, obj):
        return obj.user.count()
