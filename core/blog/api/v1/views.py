from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView  # for classbased views
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins, viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import LargeResultsSetPagination, DefaultPagination
from .filters import PostFilters


class PostList(
    ListCreateAPIView
):  # GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin
    """Getting a list of post and creating new post by class based views"""

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer  # for form in api view
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend]

    '''def get(self,request,*args , **kwargs):
        """ read and getting data """
        # queryset = self.get_queryset()
        # serializer = self.serializer_class(queryset,many=True)
        return self.list(request,*args , **kwargs)
    
    
    def post(self,request,*args , **kwargs):
        return self.create(request,*args , **kwargs)'''


class PostDetail(
    RetrieveUpdateDestroyAPIView
):  # GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin
    """Getting a list of post and creating new post by class based views"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    lookup_field = "id"  # mishe tu urls.py ham 'pk' dad behesh


"""    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)"""


# example of viewset in class based view
class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category','author','status']    #Normal
    filterset_fields = {
        "category": ["exact", "in"],
        "author": ["exact"],
        "status": ["exact"],
    }  # view filtering
    # filterset_fields = PostFilters   #based on filters.py filtering(it like up but it defines in different classes)
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination

    @action(methods=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail": "OK"})

    # def list(self,request):
    #     serializer = self.serializer_class(self.queryset,many=True)
    #     return Response(serializer.data)

    # def retrieve(self,request,pk=None):
    #     post_object = get_object_or_404(self.queryset,pk=pk)
    #     serializer = self.serializer_class(post_object)
    #     return Response(serializer.data)

    # def create(self,request):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


'''class PostList(APIView):
    """ Getting a list of post and creating new post by class based views"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer  #for form in api view
    def get(self,request):
        """ read and getting data """
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    def post(self,request):
        """ Creating post with provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''


'''class PostDetail(APIView):
    """ Getting detail of post and edit or delete it"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    def get(self,request,id):
        """ retrieving the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    def put(self,request,id):
        """ editing the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        serializer = self.serializer_class(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        """ deleting the post data """
        post = get_object_or_404(Post,pk=id,status=True)
        post.delete()
        return Response({"detail":"Item removed successfully"},status=status.HTTP_204_NO_CONTENT)'''


######### function based views for api ############

"""@api_view(["GET","POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def PostList(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def PostDetail(request,id):
    # try:
    #     post = Post.objects.get(pk=id)
    #     serializer = PostSerializer(post)
    #     return Response(serializer.data)
    # except Post.DoesNotExist:
    #     return Response({"detail":"Post does not exist"}, status=status.HTTP_404_NOT_FOUND)  #status=404
    post = get_object_or_404(Post,pk=id)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail":"Item removed successfully"},status=status.HTTP_204_NO_CONTENT)"""
