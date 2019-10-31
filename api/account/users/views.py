#python imports
from random import randint 

#django/rest_framework imports
from django.shortcuts import render,HttpResponse
from django.db import IntegrityError
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.conf import settings
from django.db import IntegrityError

# app level imports
from .models import User
from .serializers import (
    UserRegSerializer,
    UserLoginRequestSerializer,
    UserPassUpdateSerializer,

)
from libs.constants import (
    BAD_REQUEST,
    BAD_ACTION,
    BAD_USER,
    BAD_OTP
)
from libs import (
    redis_client,
    generate_pass,
    crypto,
    mail,
    message,
)
from libs.exceptions import (
    ParseException
)
from libs.cryptoClass import Crypto



class UserViewSet(GenericViewSet):
    '''
    '''
    serializers_dict = {
       'register': UserRegSerializer,
       'login': UserLoginRequestSerializer,    
       'resetpassword': UserPassUpdateSerializer 
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION,errors=key)

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)
        
        try:
            user = serializer.save()
        except Exception as e:
            return Response(({'status':'Failed','detail':str(e.args)}), status=status.HTTP_409_CONFLICT)

        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response({}, status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        """
        if request.session.has_key('user_email'):
            """
            To check wheter session is active.
            """
            return Response(({'status':'you already logged in'}), status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            print(serializer.is_valid())
            if serializer.is_valid() is False:
               raise ParseException(BAD_REQUEST, serializer.errors)

            request.session['user_email'] = serializer.validated_data['email']
            return Response(({'status':'login successfull'}), status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def logout(self, request):
        """
        Delete session
        """
        if request.session.has_key('user_email'):
            del request.session['user_email']
            return Response(({'status':'success'}), status=status.HTTP_200_OK)
        return Response(({'status':'not logged in'}), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def sendotp(self, request):
        """
        send otp to mail.
        """
        # print(request.POST.get('email', False))
        try:
            email = request.data["email"]
            if not User.objects.filter(email=email).exists():
                return Response(BAD_USER, status=status.HTTP_400_BAD_REQUEST)

            otp = randint(1000,9999)
            """
            save otp in redis.
            """
            redis_client.store_key_data(email, otp)
            """
            send mail.
            """
            subject = 'G-store otp'
            mail.sendmail.delay(message.txt_otp_message(otp), subject, [email])
            return Response(({'status':'otp sent to mail'}), status=status.HTTP_200_OK)
        except:
            return Response(BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False)
    def resetpassword(self, request):
        """
        reset or upate password.
        """
        email = request.data['email']
        otp = request.data['otp']

        if not User.objects.filter(email=email).exists():
            return Response(BAD_USER, status=status.HTTP_400_BAD_REQUEST)

        self.objects = User.objects.get(email=email)

        print(redis_client.key_exists(email))
        if not redis_client.key_exists(email):
            return Response(BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        if not redis_client.get_key_data(email).decode("utf-8") == str(otp):
            return Response(BAD_OTP, status=status.HTTP_400_BAD_REQUEST)

        # delete existing value in redis.
        redis_client.remove_key_data(email)

        serializer = self.get_serializer(self.objects, data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

        serializer.save()
        return Response(({'status':'password updated successfully'}), status=status.HTTP_200_OK)
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)


    # @action(methods=['post'],detail=False)
    # def save(self,request):
        """
        """

        # password = {request.data['email']:request.data['password']}
        # key = request.data['email']
        # hashName = key


        # # redis_client.store_data(hashName,password)
        # redis_client.remove_data(hashName,key)
        # return Response(({'detail':redis_client.get_data(hashName)}), status=status.HTTP_200_OK)

        # key = 'name'
        # value = 'raju_nadaf'
        # conn_radis.set(key,value)
        # return Response({'data':'saved'})



    # @action(methods=['post'],detail=False)
    # def delete(self,request):

        # hashName = "Authors"
        # key=request.data['key']

        # redis_client.remove_data(hashName,key)
        # return Response(({'detail':redis_client.get_data(hashName)}), status=status.HTTP_200_OK)

       # key = 'name'
       # result = conn_radis.get(key)
       # return Response({'detail':result})


