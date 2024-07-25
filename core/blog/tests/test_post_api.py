import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import User,Profile



@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email = "ali@adli.com" , password = "Novin135180", is_verified = True)
    return user
    
    
    
    
@pytest.mark.django_db
class TestPostApi:
    
    def test_get_post_response_200(self,api_client):
        url = reverse("blog:api-v1:post-list")
        respone = api_client.get(url)
        assert respone.status_code == 200
        
    def test_create_post_response_401(self,api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            'title' : 'test',
            'content' : 'description',
            'status' : True,
            'published_date' : datetime.now()
            }
        # api_client.force_authenticate(user = {})
        response = api_client.post(url , data)
        assert response.status_code == 401
        
    def test_create_post_response_201(self,api_client,common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            'title' : 'test',
            'content' : 'description',
            'status' : True,
            'published_date' : datetime.now()
            }
        user = common_user
        # api_client.force_login(user = user)
        api_client.force_authenticate(user = user)
        response = api_client.post(url , data)
        assert response.status_code == 201
        
    def test_create_post_invalid_data_response_201(self,api_client,common_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            'title' : 'test',
            'content' : 'description',
            }
        user = common_user
        # api_client.force_login(user = user)
        api_client.force_authenticate(user = user)
        response = api_client.post(url , data)
        assert response.status_code == 400
        