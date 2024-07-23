from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from .views import (
    IndexView,
    PostEdit,
    PostDelete,
    PostCreate,
    RedirectToMaktab,
    PostList,
    PostDetail,
)


app_name = "blog"

urlpatterns = [
    # path('fbv-index', indexView, name= "fbv-test"),
    # path('cbv-index', TemplateView.as_view(template_name="index.html")),
    path("cbv-index", IndexView.as_view(), name="cbv-index"),
    # path('go-to-index/', RedirectView.as_view(pattern_name = "blog:cbv-index" ), name='go-to-maktabkhooneh'),
    # path('go-to-maktabkhooneh/<int:pk>', RedirectToMaktab.as_view(),name="go-to-maktab"),
    path("post/", PostList.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("post/create/", PostCreate.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", PostEdit.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", PostDelete.as_view(), name="post-delete"),
    path("api/v1/", include("blog.api.v1.urls")),
]
