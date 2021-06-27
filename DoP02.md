# DoP02

# 一、DoP02简介

DoP01

- django1.11.11+djangorestframework3.9.0实现restful风格的API。（DRF版）
- 具体实施步骤

# 二、P02项目实施

## 1、P02

### （0）创建虚拟环境

```bash
mkvirtualenv -p python3 py3_drf
pip install -r requirements.txt
# requirements.txt
Django==1.11.11
djangorestframework==3.9.0
PyMySQL==1.0.2
```

### （1）新建项目

```bash
django-admin startproject P02
```

### （2）新建应用

```bash
cd P02
python manage.py startapp booktest
```

### （3）配置文件

1）P01/init.py

```python
import pymysql
pymysql.install_as_MySQLdb()
```

2）settings.py

```python
# 注册应用
	'rest_framework',  # DRF应用
    'booktest',  # 图书应用

# 注销crsf
    # 'django.middleware.csrf.CsrfViewMiddleware',

# 配置mysql数据库。
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "test1",
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root',
# 提示：需要手动创建test1数据库。

# 时区、语言 本地化
LANGUAGE_CODE = 'zh-Hans' # 设置汉语显示
TIME_ZONE = 'Asia/Shanghai' # 设置具体时区，配合USE_TZ使用
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 使用非美国时区

```

3）SQL创建数据库test1命令

```sql
-- 0 创建数据库test1
CREATE DATABASE IF NOT EXISTS test1 DEFAULT CHARSET utf8;
USE test1;
```



### （4）编写模型类models.py，迁移，添加数据

1）模型类

```python
from django.db import models


# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(blank=True, null=True)
    bcomment = models.IntegerField(blank=True, null=True, verbose_name='评论量')
    is_delete = models.IntegerField(default=False)

    def __str__(self):
        return self.btitle


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.IntegerField()
    hcontent = models.CharField(max_length=100)
    hbook = models.ForeignKey("Bookinfo")
    is_delete = models.IntegerField(default=False)

    def __str__(self):
        return self.hname

```

2）迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

3）添加数据

```sql
-- 1 
insert into booktest_bookinfo(btitle,bpub_date,bread,bcomment,is_delete) values
('射雕英雄传','1980-5-1',12,34,0),
('天龙八部','1986-7-24',36,40,0),
('笑傲江湖','1995-12-24',20,80,0),
('雪山飞狐','1987-11-11',58,24,0);

-- 2
insert into booktest_heroinfo(hname,hgender,hbook_id,hcontent,is_delete) values
('郭靖',1,1,'降龙十八掌',0),
('黄蓉',0,1,'打狗棍法',0),
('黄药师',1,1,'弹指神通',0),
('欧阳锋',1,1,'蛤蟆功',0),
('梅超风',0,1,'九阴白骨爪',0),
('乔峰',1,2,'降龙十八掌',0),
('段誉',1,2,'六脉神剑',0),
('虚竹',1,2,'天山六阳掌',0),
('王语嫣',0,2,'神仙姐姐',0),
('令狐冲',1,3,'独孤九剑',0),
('任盈盈',0,3,'弹琴',0),
('岳不群',1,3,'华山剑法',0),
('东方不败',0,3,'葵花宝典',0),
('胡斐',1,4,'胡家刀法',0),
('苗若兰',0,4,'黄衣',0),
('程灵素',0,4,'医术',0),
('袁紫衣',0,4,'六合拳',0);
```

### （5）编写序列化器

booktest/serializers.py

```python
from rest_framework import serializers
from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    '''自定义序列化器'''

    class Meta:
        model = BookInfo  # 指定序列化器从哪个模型映射字段
        fields = "__all__"  # 映射哪些字段
```



### （6）编写视图views.py

booktest/views.py

```python
from rest_framework.viewsets import ModelViewSet

from .models import BookInfo
from .serializers import BookInfoSerializer

class BookInfoView(ModelViewSet):
    '''定义视图类'''
    # 指定查询集
    queryset = BookInfo.objects.all()
    # 指定序列化器
    serializer_class = BookInfoSerializer
```

### （7）配置路由urls.py

P02/urls.py

```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('booktest.urls')),  # 书籍模块
]
```

booktest/urls.py

```python
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
]
router = DefaultRouter()
router.register(r'books', views.BookInfoView)
urlpatterns += router.urls
```

