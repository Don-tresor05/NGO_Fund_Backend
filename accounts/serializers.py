import datetime
from rest_framework import serializers
from accounts.models import VerificationCode
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializers(serializers.ModelSerializer):
    re_password=serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['re_password'] != data['password']:
            raise serializers.ValidationError("Password and Confirm Password does not match")
        return data
    
    class Meta:
        model=User
        fields=(
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            're_password',
            'phone_number',
            'is_active',
            'user_type',
        )

        extra_kwargs={"password": {"write_only": True}, "re_password": {"write_only": True}}

    def create(self, validated_data):
        user=User.objects.create_user(
            email=self.validated_data['email'], first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'], password=self.validated_data['password'],
            phone_number=self.validated_data.get('phone_number'),
            user_type=self.validated_data.get('user_type','DONOR'),
        )
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        User.objects.filter(id=user.id).update(last_login=datetime.datetime.now())

        user.save()
        token = super().get_token(user)

        # Add custom claims

        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        token['user_type'] = user.user_type
        return token