from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from .views import PostList, PostDetail, PostModelViewSet, CategoryModelViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register("post", PostModelViewSet, basename="post")
router.register("category", CategoryModelViewSet, basename="category")

app_name = "api-v1"

urlpatterns = router.urls


# urlpatterns = [
#     path("post/",PostViewSet.as_view({'get':'list','post':'create'}),name='post-list'),
#     path("post/<int:pk>/",PostViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}),name='post-detail')
#     # path('post/',PostList.as_view(),name = "post-list"),
#     # path('post/<int:id>/',PostDetail.as_view(),name = "post-list"),
# ]
