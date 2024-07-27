from rest_framework import generics
from .serializers import (
    ActivationResendSerializer,
    RegistrationSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    TokenCustomObtainPairSerializer,
    CustomAuthTokenSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# from accounts.models import User #one way to use user model
from django.contrib.auth import get_user_model  # another way to import user model
from ...models import Profile
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from mail_templated import send_mail, EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email": email,
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation.tpl", {"token": token}, "admin@admin.com", to=[email]
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
        # return self.create(request,*args,**kwargs)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenCustomObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    """
    An end point for changing password
    """

    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # checking old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "[wrong password]"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password has changed successfully!"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    """
    retrieving name,lastname from user
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        print(self.request.user)
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    # def get_queryset(self):
    #     return super().get_queryset()


class TestEmailSend(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # send_mail( #with common
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )
        # send_mail("email/hello.tpl",{"name":"Novuuuu"},"admin@admin.com",["Novini.n1380@gmail.com"])  #using mail_templated
        self.email = "Novini.n1380@gmail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/hello.tpl", {"token": token}, "admin@admin.com", to=[self.email]
        )
        EmailThread(email_obj).start()
        return Response("email sent")

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            # decode -> id user
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        # if token  not valid
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        # object user
        user_obj = User.objects.get(pk=user_id)
        # is_verified -> true
        user_obj.is_verified = True
        # if openned again
        if user_obj.is_verified:
            return Response(
                {"details": "your account has already been verified and activated!"},
                status=status.HTTP_200_OK,
            )
        # saving form
        user_obj.save()
        # if token valid response ok
        return Response(
            {"details": "your account have been verified and activated successfully!"},
            status=status.HTTP_200_OK,
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )
        # else:
        #     return Response({"details":"invalid request"},status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
