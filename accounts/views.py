from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, status
from accounts.models import User
from accounts.permissions import IsRegistrar
from accounts.serializers import CustomTokenObtainPairSerializer, UserSerializers
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.decorators import action
# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes=[IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer=self.serializer_class(self.queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method=="POST":
            return [AllowAny()]
        elif self.action =="list":
            return[IsRegistrar()]
        return super().get_permissions()
    
    @action(["get"], detail=False)
    def profile(self,request):
        serializer=self.get_serializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
    def create(self, request, *args, **kwargs):
        serializers = UserSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        
        # Return different messages based on user type
        if user.user_type == 'DONOR':
            return Response({
                **serializers.data,
                "message": "Account created successfully. You can now login."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                **serializers.data,
                "message": "Account created successfully. Please wait for admin approval before you can login."
            }, status=status.HTTP_201_CREATED)

class LoginMixin(viewsets.ViewSet):
    custom_serializer = CustomTokenObtainPairSerializer
    queryset = User.objects.all()
    permission_classes = ()
 
    def create(self, request, *args, **kwargs):
        serializer = self.custom_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)