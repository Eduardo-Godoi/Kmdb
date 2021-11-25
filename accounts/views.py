from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, UserSerializer


class CreateUserView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'username': ['A user with that username already exists.']},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'Unauthorized': 'Faile to authenticate'},
                        status=status.HTTP_401_UNAUTHORIZED)
