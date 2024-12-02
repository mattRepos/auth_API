from rest_framework import serializers
from .models import User

class AuthVerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

class AuthVerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

class ActivateInvaiteCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    user_inv_code = serializers.CharField(max_length = 6)

class UserProfileSerializer(serializers.ModelSerializer):
    user_with_my_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'user_inv_code', 'activated_inv_code', 'user_with_my_code']

    def get_user_with_my_code(self,obj):
        users = User.objects.filter(activated_inv_code=obj.user_inv_code)
        return [user.phone_number for user in users]
        
