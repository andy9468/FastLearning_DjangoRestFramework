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
