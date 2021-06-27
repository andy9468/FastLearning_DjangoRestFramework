import sys
import json
import datetime

from django.test import TestCase

from .models import BookInfo


# Create your tests here.
# 模型测试
class BookInfoModelsTest(TestCase):
    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        # 测试前新增一条数据
        BookInfo.objects.create(btitle='经济全球化', bpub_date='2021-12-12', bread=0, bcomment=0, is_delete=False)

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def tearDown(self):
        print("测试结束")
        pass

    # 测试新增数据
    def test_create(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 新增一条数据
        BookInfo.objects.create(btitle='经济全球化2', bpub_date='2022-12-12', bread=2, bcomment=2, is_delete=False)

        # 测试新增结果
        book = BookInfo.objects.get(btitle='经济全球化2')
        self.assertEqual(book.btitle, "经济全球化2")
        self.assertEqual(book.bpub_date, datetime.date(2022, 12, 12))
        self.assertEqual(book.bread, 2)
        self.assertEqual(book.bcomment, 2)
        self.assertEqual(book.is_delete, False)

    # 测试物理删除
    def test_delete(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 删除数据
        book = BookInfo.objects.get(btitle='经济全球化')
        book.delete()

        # 测试删除结果
        bs = BookInfo.objects.filter(btitle='经济全球化')
        self.assertEqual(len(bs), 0)

    # 测试逻辑删除
    def test_delete_on_logic(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 逻辑删除数据
        book = BookInfo.objects.get(btitle='经济全球化')
        book.is_delete = True
        book.save()

        # 测试逻辑删除结果
        bs = BookInfo.objects.filter(btitle='经济全球化', is_delete=True)
        self.assertEqual(len(bs), 1)

    # 测试单条查询、多条查询
    def test_query(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 额外新增一条数据
        BookInfo.objects.create(btitle='经济全球化3', bpub_date='2023-12-12', bread=3, bcomment=3, is_delete=False)

        # 单条查询，并测试结果
        book = BookInfo.objects.get(btitle="经济全球化3")
        self.assertEqual(book.btitle, "经济全球化3")
        self.assertEqual(book.bpub_date, datetime.date(2023, 12, 12))
        self.assertEqual(book.bread, 3)
        self.assertEqual(book.bcomment, 3)
        self.assertEqual(book.is_delete, False)

        # 多条查询，并测试结果
        books = BookInfo.objects.filter(btitle__contains="经济全球化")
        self.assertEqual(len(books), 2)


# 视图测试
class BookInfoViewsTest(TestCase):
    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        # 测试前新增一条数据
        BookInfo.objects.create(btitle='经济全球化5', bpub_date='2025-12-12', bread=5, bcomment=5, is_delete=False)

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def tearDown(self):
        print("测试结束")

    # 测试单条、多条查询。get  /books/%s/   get  /books/
    def test_books_get(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 额外新增一条数据
        book_again = BookInfo.objects.create(btitle='经济全球化6', bpub_date='2026-12-12', bread=6, bcomment=6,
                                             is_delete=False)

        # 单条查询
        response_one = self.client.get('/books/%s/' % book_again.id)  # 发出请求。查询单条数据
        json_one = response_one.json()
        # 测试单条数据
        self.assertEqual(response_one.status_code, 200)
        self.assertEqual(json_one["btitle"], "经济全球化6")
        self.assertEqual(json_one["bpub_date"], "2026-12-12")
        self.assertEqual(json_one["bread"], 6)
        self.assertEqual(json_one["bcomment"], 6)
        self.assertEqual(json_one["is_delete"], False)

        # 多条查询
        response_many = self.client.get('/books/')  # 发出请求。查询多条数据
        book_list = response_many.json()
        # 测试多条数据
        self.assertEqual(response_many.status_code, 200)
        self.assertEqual(len(book_list), 2)

    # 测试新增。post  /books/
    def test_books_post(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 新增数据
        front_dict = {
            "btitle": "经济全球化7",
            "bpub_date": "2027-12-12",
            "bread": 7,
            "bcomment": 7,
            "is_delete": False
        }
        front_dict_str = json.dumps(front_dict, ensure_ascii=False)  # 字典转成str字串

        response_one = self.client.post("/books/", data=front_dict_str, content_type='application/json')  # 发出请求。新增数据
        json_one = response_one.json()
        # 测试新增数据
        self.assertEqual(response_one.status_code, 201)
        self.assertEqual(json_one['btitle'], front_dict['btitle'])

    # 测试修改。put /books/%s/
    def test_books_put(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 额外新增一条数据
        book_again = BookInfo.objects.create(btitle='经济全球化8', bpub_date='2028-12-12', bread=8, bcomment=8,
                                             is_delete=False)
        # 构造修改数据
        front_dict = {
            "btitle": "经济全球化80",
            "bpub_date": "2008-12-12",
            "bread": 80,
            "bcomment": 80,
            "is_delete": False
        }
        front_dict_str = json.dumps(front_dict, ensure_ascii=False)  # 字典转成str字串

        response_one = self.client.put("/books/%s/" % book_again.id, data=front_dict_str,
                                       content_type='application/json')  # 发出请求。修改数据
        json_one = response_one.json()

        # 测试新增数据
        self.assertEqual(response_one.status_code, 203)
        self.assertEqual(json_one['btitle'], front_dict['btitle'])

    # 测试删除。delete /books/%s/
    def test_books_delete(self):
        print("测试开始：%s" % (sys._getframe().f_code.co_name))
        # 额外新增一条数据
        book_again = BookInfo.objects.create(btitle='经济全球化9', bpub_date='2029-12-12', bread=9, bcomment=9,
                                             is_delete=False)

        response_one = self.client.delete("/books/%s/" % book_again.id)  # 发出请求。删除数据
        content = response_one.content.decode()
        # 测试新增数据
        self.assertEqual(response_one.status_code, 204)
        self.assertEqual(len(content), 0)
