from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import (
    DeleteView,
    UpdateView,
    CreateView,
    FormView,
    ListView,
    TemplateView,
    RedirectView,
    DetailView,
)
from .models import Post, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm, PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.

# Create your views here.

# Function Base View show a template
''' 
def indexView(request):
    """
    a function based view to show index page
    """
    name = "ali"
    context = {"name":name}
    return render(request,"index.html",context)
'''


class IndexView(TemplateView):
    """
    a class based view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context


""" FBV or redirect 

def redirectToMaktab(requset):
    return redirect('https://maktabkhooneh.com')
    
"""


class RedirectToMaktab(RedirectView):
    url = "https://maktabkhooneh.com"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Post
    """  type of model definition  """
    # queryset = Post.objects.all()
    # def get_queryset(self):
    #     posts = Post.objects.filter(status = True)
    #     return posts
    context_object_name = "posts"
    paginate_by = 2
    ordering = "-id"
    permission_required = "blog.view_post"


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post


"""    
class PostCreate(FormView):
    template_name = 'contact.html'
    form_class = PostForm
    success_url = '/blog/post/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)"""


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    """  this is two ways to identify fields to project  """
    form_class = PostForm
    # fields = ['author','title','content','status','category','published_date']
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDelete(DeleteView):
    model = Post
    success_url = "/blog/post/"
