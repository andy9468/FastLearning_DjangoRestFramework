from rest_framework.viewsets import ModelViewSet

from .models import BookInfo
from .serializers import BookInfoSerializer


class BookInfoView(ModelViewSet):
    '''定义视图类'''
    # 指定查询集
    queryset = BookInfo.objects.all()
    # 指定序列化器
    serializer_class = BookInfoSerializer
