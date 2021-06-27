from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [

]
router = DefaultRouter()
router.register(r'books', views.BookInfoView)
urlpatterns += router.urls
