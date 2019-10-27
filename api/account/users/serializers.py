#python imports
import re

#django/rest_framework imports
from rest_framework import serializers

#app level imports
from .models import User

from libs import(
 generate_pass,
 mail,
 message,
 crypto,
 )

class UserRegSerializer(serializers.ModelSerializer):
    '''
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)
    mobile = serializers.IntegerField(
        required=True,
        min_value=5000000000,
        max_value=9999999999
    )

    class Meta:
        model = User
        fields = ('id', 'password', 'first_name', 'last_name', 'email', 'mobile', 'address','full_name',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self,validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            mobile=validated_data['mobile'],
            address=validated_data['address']
  
            )
        user.save()
        subject = "G-strore User Registration Confirmation"
        mail.sendmail(message.text_message(user.first_name,crypto.decrypt(user.password)),subject,[user.email])
        return user

    def validate(self, data):
        # print(crypto.encrypt(b'rajuna'))
        extra = {'password':crypto.encrypt(generate_pass.generatePass().encode())}
        data.update(extra)
        return data

        

class UserLoginRequestSerializer(serializers.ModelSerializer):
    '''
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=2)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_admin', 'is_active',)


    def validate(self, data):
        """
        To validated email and password.
        """
        pattern = "^(?!\.)[^. \n]+$"
        valid_password = re.findall(pattern, data['password'])
        """
        If Valid Passwod is Empty.! when password contain space or any spacial charactre in first.
        """
        if not valid_password:
            raise serializers.ValidationError('Invalid Password')

        try:
            user = User.objects.get(
                email = data["email"],
                password = crypto.encrypt(data["password"].encode())
                
                )
        except:
            raise serializers.ValidationError('Invalid Credential')

        return data

class UserPassUpdateSerializer(serializers.ModelSerializer):
    '''
    Reset or Update the password.
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields =('id', 'email', 'password',)

    def validate(self, data):
        pattern = "^(?!\.)[^. \n]+$"
        valid_password = re.findall(pattern, data['password'])
        if not valid_password:
            raise serializers.ValidationError('Invalid Password')

        return data

    def update(self, instance, validated_data):
        '''
        '''
        if 'password' in validated_data:
            # instance.password =crypto.encrypt(validated_data.get('password', instance.password).encode())
            instance.password =crypto.encrypt(validated_data.get('password').encode())
        instance.save()
        return instance







