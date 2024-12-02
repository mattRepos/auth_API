import random
import secrets
import string
import logging

from time import sleep

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import AuthVerifyPhoneNumberSerializer, AuthVerifyCodeSerializer, UserProfileSerializer, ActivateInvaiteCodeSerializer

AUTH_CODES = {}
logger = logging.getLogger(__name__)

class AuthRequestView(APIView):
    @swagger_auto_schema(
        request_body=AuthVerifyPhoneNumberSerializer,
        responses={200: 'Code was sent'}
    )
    def post(self, request):
        logger.debug("AuthRequestView called")
        serializer = AuthVerifyPhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = f'{secrets.randbelow(999999)}'
        AUTH_CODES[phone_number] = code

        sleep(2)
        print(f"Generated code for {phone_number}: {code}")
        return Response({'message': 'Code was sent'}, status=status.HTTP_200_OK)

class VerifyProfileView(APIView):
    @swagger_auto_schema(
        request_body=AuthVerifyCodeSerializer,
        responses={200: 'Successful login'}
    )
    def post(self, request):
        logger.debug("VerifyProfileView called")
        serializer = AuthVerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        if AUTH_CODES.get(phone_number) == code:
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.user_inv_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                print(f"Generated invite code for {phone_number}: {user.user_inv_code}")
                user.save()
                return Response({'message': 'Successful login'}, status=status.HTTP_200_OK)
            return Response({'message': 'Successful login'}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('phone_number', openapi.IN_QUERY, description="Phone number", type=openapi.TYPE_STRING)],
        responses={200: UserProfileSerializer, 404: 'User not found'}
    )
    def get(self, request):
        logger.debug("ProfileView called")
        phone_number = f'+{request.query_params.get('phone_number')}'.replace(' ', '')
        try:
            user = User.objects.get(phone_number=phone_number)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ActInvaiteCodeView(APIView):
    @swagger_auto_schema(
        request_body=ActivateInvaiteCodeSerializer,
        responses={200: 'Invite code activated', 400: 'Invite code already activated', 404: 'Invalid invite code or User not found'}
    )
    def post(self, request):
        logger.debug("ActInvaiteCodeView called")
        serializer = ActivateInvaiteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_inv_code = serializer.validated_data['user_inv_code']
        phone_number = serializer.validated_data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
            if user.activated_inv_code:
                return Response({'error': 'Invite code already activated'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(user_inv_code=user_inv_code):
                user.activated_inv_code = user_inv_code
                user.save()
                return Response({'message': 'Invite code activated'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
