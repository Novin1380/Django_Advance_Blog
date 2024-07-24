from django.test import TestCase,SimpleTestCase,Client
from django.urls import reverse,resolve
from accounts.models import User,Profile
from ..models import Post,Category
from datetime import datetime


class TestBlogViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email= 'test@test.com',password = "Novin135180")
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = "test",
            last_name = "test",
            description = "desc"
            )
        self.post = Post.objects.create(
            author = self.profile,
            title = 'test',
            content = 'description',
            status = True,
            category = None,
            published_date = datetime.now()
            )
        
        
    def test_blog_index_url__successfull_response(self):
        url = reverse("blog:index")
        respone = self.client.get(url)
        self.assertEquals(respone.status_code,200)
        self.assertTrue(str(respone.content).find('index'))
        self.assertTemplateUsed(respone,template_name='index.html')
        
    def test_blog_post_detail_logged_in_response(self):
        self.client.force_login(user = self.user)
        url = reverse("blog:post-detail",kwargs= {'pk':self.post.id})
        respone = self.client.get(url)
        self.assertEquals(respone.status_code,200)
    
    
    def test_blog_post_detail_annonymous_response(self):
        url = reverse("blog:post-detail",kwargs= {'pk':self.post.id})
        respone = self.client.get(url)
        self.assertEquals(respone.status_code,302)
