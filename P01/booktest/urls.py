from django.conf.urls import url
from . import views

urlpatterns = [
    # 列表视图路由
    url(r'^books/$', views.BookListView.as_view()),
    # 详情视图路由
    url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view()),
]
