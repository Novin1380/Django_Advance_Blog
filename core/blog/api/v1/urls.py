from django.urls import path,include
from django.views.generic import TemplateView,RedirectView
from .views import  PostList,PostDetail


app_name= 'api-v1'

urlpatterns = [
    path('post/',PostList,name = "post-list"),
    path('post/<int:id>/',PostDetail,name = "post-list"),
]