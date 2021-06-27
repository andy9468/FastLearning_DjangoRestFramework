import json

from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views import View

from .models import BookInfo


class BookListView(View):
    '''列表视图'''

    def get(self, request):
        '''查询所有图书接口'''
        # 1，查询集
        books = BookInfo.objects.all()

        # 2，遍历查询集。并且将模型转成dict字典，放到list列表中
        book_list = []
        for book in books:
            # 将模型转成dict字典
            book_dict = {
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'is_delete': book.is_delete
            }
            # 放到list列表中
            book_list.append(book_dict)

        # 3，响应
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        '''新增图书接口'''
        # 1，获取前端数据。并转成dict字典
        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        front_dict = json.loads(json_str)

        # 2，创建模型对象。并入库
        book = BookInfo(
            btitle=front_dict['btitle'],
            bpub_date=front_dict['bpub_date'],
            bread=front_dict.get('bread', 0),
            bcomment=front_dict.get('bcomment', 0)
        )
        book.save()

        # 3，新增数据转成字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete
        }

        # 4，响应
        return JsonResponse(book_dict, status=201)


class BookDetailView(View):
    '''详情视图'''

    def get(self, request, pk):
        '''查询指定id图书接口'''
        # 1，获取查询集
        try:
            books = BookInfo.objects.filter(Q(id=pk) & Q(is_delete=False))
            book = books[0]
        except Exception as e:
            return JsonResponse({'message': '查不到数据'}, status=404)

        # 2，模型转字典dict
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete
        }

        # 3，响应
        return JsonResponse(book_dict)

    def put(self, request, pk):
        '''修改指定id图书接口'''
        # 1，获取查询集
        try:
            book = BookInfo.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({'message': '查不到数据'}, status=404)

        # 2，获取前端数据，并转字典
        front_str_bytes = request.body
        front_str = front_str_bytes.decode()
        front_dict = json.loads(front_str)

        # 3，重新给模型指定属性赋值
        book.btitle = front_dict.get('btitle', book.btitle)
        book.bpub_date = front_dict.get('bpub_date', book.bpub_date)
        book.bread = front_dict.get('bread', book.bread)
        book.bcomment = front_dict.get('bcomment', book.bcomment)
        book.is_delete = front_dict.get('is_delete', book.is_delete)

        # 4，入库保存
        book.save()

        # 5，模型转字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'is_delete': book.is_delete
        }

        # 6，响应
        return JsonResponse(book_dict, status=203)

    def delete(self, request, pk):
        '''删除指定id图书接口'''
        # 1，查询集
        try:
            books = BookInfo.objects.filter(Q(id=pk) & Q(is_delete=False))
            book = books[0]
        except Exception as e:
            return JsonResponse({'message': '查不到数据'}, status=404)

        # 2，删除
        # 逻辑删除
        book.is_delete = True
        book.save()

        # 物理删除
        # book.delete()

        # 3，响应状态码204
        return HttpResponse(status=204)
