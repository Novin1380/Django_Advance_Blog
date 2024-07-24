from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from ..forms import PostForm
from datetime import datetime
from ..models import Category


#checking form is valid or not


class TestPostForm(TestCase):
    
    def test_post_form_with_valid_data(self):
        category_obj = Category.objects.create(name = "hello")
        form = PostForm(data = {
            'title':'test',
            'content':'description',
            'status':True,
            'category':category_obj,
            'published_date':datetime.now()
        })
        self.assertTrue(form.is_valid())
        
        
    def test_post_form_with_no_data(self):
        form = PostForm(data = {})
        self.assertFalse(form.is_valid())