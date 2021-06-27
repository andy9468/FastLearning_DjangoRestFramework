from rest_framework import serializers
from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    '''自定义序列化器'''

    class Meta:
        model = BookInfo  # 指定序列化器从哪个模型映射字段
        fields = "__all__"  # 映射哪些字段
