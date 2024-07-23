from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from .views import (
    ActivationResendApiView,
    RegistrationApiView,
    TestEmailSend,
    ActivationApiView,
    ProfileApiView,
    CustomObtainAuthToken,
    ChangePasswordApiView,
    CustomDiscardAuthToken,
    CustomTokenObtainPairView,
)

# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "api-v1"

urlpatterns = [
    # resgistration
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path("test-mail/", TestEmailSend.as_view(), name="test-mail"),
    # activation
    path(
        "activation/confirm/<str:token>", ActivationApiView.as_view(), name="activation"
    ),
    # re-send activation
    path("activation/resend/", ActivationResendApiView.as_view(), name="re-send"),
    # login token
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    # path("token/login",ObtainAuthToken.as_view() , name = 'token-login')
    # logout token
    path("token/logout/", CustomDiscardAuthToken.as_view(), name="token-logout"),
    # login JWT
    # path('jwt/create/',TokenObtainPairView.as_view(),name="jwt-create"),
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # change password
    path("change-password", ChangePasswordApiView.as_view(), name="change-password"),
    # reset password
    # Profile
    path("profile/", ProfileApiView.as_view(), name="profile"),
]
