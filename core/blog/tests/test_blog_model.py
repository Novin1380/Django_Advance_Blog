from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from ..models import Post,Category
from datetime import datetime
from django.contrib.auth import get_user_model
from accounts.models import User,Profile





class TestPostModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email= 'test@test.com',password = "Novin135180")
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = "test",
            last_name = "test",
            description = "desc"
        )

    
    def test_create_post_with_valid_data(self):
        
        post = Post.objects.create(
            author = self.profile,
            title = 'test',
            content = 'description',
            status = True,
            category = None,
            published_date = datetime.now()
            )
        self.assertEquals(post.title,'test')
        self.assertTrue(Post.objects.filter(pk = post.id).exists())
        
#One way to create it without using setup function
# class TestPostModel(TestCase):
    
#     def test_create_post_with_valid_data(self):
#         user = User.objects.create_user(email= 'test@test.com',password = "Novin135180")
#         profile = Profile.objects.create(
#             user = user,
#             first_name = "test",
#             last_name = "test",
#             description = "desc"
#         )
#         post = Post.objects.create(
#             author = profile,
#             title = 'test',
#             content = 'description',
#             status = True,
#             category = None,
#             published_date = datetime.now()
#             )
#         self.assertEquals(post.title,'test')