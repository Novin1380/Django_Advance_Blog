from django.urls import path,include
from django.views.generic import TemplateView,RedirectView
from .views import RegistrationApiView,CustomObtainAuthToken,CustomDiscardAuthToken
# from rest_framework.authtoken.views import ObtainAuthToken


app_name= 'api-v1'

urlpatterns = [
    #resgistration
    path('registration/',RegistrationApiView.as_view(), name='registration'),
    #login token
    path('token/login/',CustomObtainAuthToken.as_view(), name='token-login'),
    # path("token/login",ObtainAuthToken.as_view() , name = 'token-login')
    #logout token
    path('token/logout/',CustomDiscardAuthToken.as_view(), name='token-logout'),
    #change password
    #reset password
    #
    


]