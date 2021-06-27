# DoP01

# 一、DoP01简介

DoP01

- django1.11.11实现原始版restful风格的API。
- 具体实施步骤

# 二、P01项目实施

## 1、P01

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
django-admin startproject P01
```

### （2）新建应用

```bash
cd P01
python manage.py startapp booktest
```

### （3）配置文件

1）P01/init.py

```
import pymysql
pymysql.install_as_MySQLdb()
```

2）settings.py

```python
# 注册应用
	'booktest',

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

### （5）编写视图views.py

```python
import json

from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views import View

from .models import BookInfo


class BookListView(View):
    '''列表视图'''

    def get(self, request):
        '''查询所有图书接口'''
        # 1.查询所有书籍模型的查询集
        books = BookInfo.objects.all()

        # 2.遍历查询集，取出里面的每个书籍模型对象，把模型对象转为字典
        # 定义一个列表变量，用来保存所有字典
        book_list = []
        for book in books:
            book_dict = {
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'is_delete': book.is_delete,
            }
            book_list.append(book_dict)  # 将转换好的字典添加到列表中

        # 3.响应
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        '''新增图书接口'''
        # 获取前端传入的请求体数据（json）
        json_str_bytes = request.body
        # 把bytes类型转成json字符串json_str
        json_str = json_str_bytes.decode()
        # 利用json.loads将json字符串转换成dict（字典、列表）
        book_dict = json.loads(json_str)
        # 创建模型对象并保存（把字典转换成模型并存储）
        book = BookInfo(
            btitle=book_dict['btitle'],
            bpub_date=book_dict['bpub_date'],
            bread=book_dict.get("bread", 0),
            bcomment=book_dict.get("bcomment", 0)
        )
        book.save()

        # 把新增的模型转为字典
        json_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete
        }

        # 响应
        return JsonResponse(json_dict, status=201)


class BookDetailView(View):
    '''详情视图'''

    def get(self, request, pk):
        '''查询指定某个图书接口'''
        # 1.获取指定pk的那个模型
        try:
            # 查询集。查询
            books = BookInfo.objects.filter(Q(id=pk) & Q(is_delete=False))
            book = books[0]
        except Exception as e:
            return JsonResponse({'message': '查询不到数据'}, status=404)
        # 2.模型转字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete,
        }

        # 3.响应
        return JsonResponse(book_dict)

    def put(self, request, pk):
        '''修改指定图书接口'''
        # 先查询要修改的模型对象
        try:
            # 查询集。查询
            # books = BookInfo.objects.filter(Q(id=pk) & Q(is_delete=False))
            # book = books[0]
            book = BookInfo.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({'message': '查询不到数据'}, status=404)

        # 获取前端传入的新数据（把数据转为字典）
        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        book_dict = json.loads(json_str)

        # 重新给模型指定的属性赋值
        book.btitle = book_dict['btitle']
        book.bpub_date = book_dict['bpub_date']
        book.is_delete = book_dict.get('is_delete', 0)

        # 调用save方法进行修改操作
        book.save()

        # 把修改后模型转成字典
        json_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete,
        }

        # 响应
        return JsonResponse(json_dict, status=203)

    def delete(self, request, pk):
        '''删除指定图书接口'''
        try:
            # 查询集。查询
            books = BookInfo.objects.filter(Q(id=pk) & Q(is_delete=False))
            book = books[0]
        except Exception as e:
            return JsonResponse({'message': '查询不到数据'}, status=404)

        # 逻辑删除
        book.is_delete = True
        book.save()

        # 物理删除
        # book.delete()

        return HttpResponse(status=204)
```

### （6）配置路由urls.py

P01/urls.py

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
from django.conf.urls import url
from . import views
urlpatterns = [
    # 列表视图路由
    url(r'^books/$', views.BookListView.as_view()),
    # 详情视图路由
    url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view()),
]

```

