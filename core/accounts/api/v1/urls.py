from django.urls import path,include
from django.views.generic import TemplateView,RedirectView
from .views import RegistrationApiView


app_name= 'api-v1'

urlpatterns = [
    #resgistration
    path('registration/',RegistrationApiView.as_view(), name='registration')
    #change password
    #reset password
    


]