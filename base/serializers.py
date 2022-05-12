from rest_framework import serializers
from .models import Note, Category, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'owner', 'token')

    def get_token(self, obj: Profile) -> str:
        token = RefreshToken.for_user(obj.owner)
        return str(token.access_token)


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(
            style={'input_type': 'password'},
            required=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name', 'token')

    def get_token(self, obj: Profile) -> str:
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


# Custom Token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs) -> dict:
        data = super().validate(attrs)

        serializer = ProfileSerializer(self.user.profile).data
        # fields = ('id', 'name', 'email', 'username', 'user', 'token')
        for k, v in serializer.items():
            data[k] = v

        return data
