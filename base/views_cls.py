from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (NoteSerializer,
                          CategorySerializer,
                          ProfileSerializer,
                          UserSerializer,
                          MyTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Note, Category, Profile
from django.db.models import Q
from .pagination import StandardResultsSetPagination

# Create your views here.
User = get_user_model()


class NotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if params := self.request.query_params:
            if keyword := params.get('keyword', default=None):
                return Note.objects.filter(owner=self.request.user).filter(
                        Q(title__icontains=keyword)
                        | Q(body__icontains=keyword)
                )
            if pin := params.get('pin', default=None):
                try:
                    return Note.objects.filter(owner=self.request.user).filter(
                            is_pinned__exact=pin.capitalize()
                    )
                except ValidationError:
                    return []

        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    @action(detail=True, renderer_classes=[renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
    def notes(self, request, *args, **kwargs):
        notes = self.get_object().note_set.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if params := self.request.query_params:
            if name := params.get('name', default=None):
                return Category.objects.filter(owner=self.request.user).filter(
                        Q(name__icontains=name)
                )
        return Category.objects.filter(owner=self.request.user)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    http_method_names = ('get', 'head', 'options', 'put', 'delete', 'patch')

    def get_queryset(self):
        return Profile.objects.filter(owner=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ('post', 'head', 'options')

    def create(self, request, *args, **kwargs):
        data = request.data
        serialized_data = UserSerializer(data=data)
        if serialized_data.is_valid():
            try:
                user = User.objects.create(
                        username=data['username'],
                        email=data['email'],
                        first_name=data['first_name'] if data.get('first_name') else None,
                        last_name=data['last_name'] if data.get('last_name') else None,
                        password=make_password(data['password'])
                )
            except IntegrityError:
                data = {'message': 'User already registered!'}
                return Response(data, status=status.HTTP_409_CONFLICT)

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
