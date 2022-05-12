from django.db import IntegrityError
from django.db.models import Q
from django.http.request import HttpRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Note, Category
from .serializers import (NoteSerializer,
                          CategorySerializer,
                          ProfileSerializer,
                          UserSerializer,
                          MyTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(('GET',))
def get_routes(request: HttpRequest) -> Response:
    routes = {
        'routes': '/note_app/api',
        'register': '/note_app/api/users',
        'login': '/note_app/api/token/login',
        'login_refresh': '/note_app/api/token/login/refresh',
        'profile': '/note_app/api/profile',
        'the user\'s all notes': '/note_app/api/notes',
        'the user\'s single note': '/note_app/api/notes/<str:note_id>',
        'the user\'s all categories': '/note_app/api/categories',
        'the user\'s single category': '/note_app/api/categories/<str:category_id>',
        'the user\'s single category\'s notes': '/note_app/api/categories/<str:category_id>/notes',
    }

    return Response(routes)


@api_view(('GET', 'POST'))
@permission_classes((IsAuthenticated,))
def note_list(request: HttpRequest) -> Response:
    try:
        notes = Note.objects.filter(owner=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if params := request.query_params:
            if search := params.get('search', default=None):
                notes = notes.filter(
                        Q(title__icontains=search)
                        | Q(body__icontains=search)
                )
            if pin := params.get('pin', default=None):
                notes = notes.filter(
                        Q(is_pinned__exact=pin.capitalize())
                )
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data, many=False)
        if serializer.is_valid():
            print(request.data)
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET', 'PUT', 'DELETE'))
@permission_classes((IsAuthenticated,))
def single_note(request: HttpRequest, note_id: str) -> Response:
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if note.owner != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET', 'POST'))
@permission_classes((IsAuthenticated,))
def category_list(request: HttpRequest) -> Response:
    try:
        categories = Category.objects.filter(owner=request.user)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if params := request.query_params:
            if name := params.get('name', default=None):
                categories = categories.filter(
                        Q(name__icontains=name)
                )

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET', 'PUT', 'DELETE'))
@permission_classes((IsAuthenticated,))
def single_category(request: HttpRequest, category_id: str):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if category.owner != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def category_notes(request: HttpRequest, category_id: str) -> Response:
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if category.owner != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        notes = category.note_set.filter(owner=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(('POST',))
def create_user(request: HttpRequest) -> Response:
    data = request.data
    serialized_data = UserSerializer(data=data)
    if serialized_data.is_valid():
        try:
            user = User.objects.create(
                    username=data['username'],
                    email=data['email'],
                    password=make_password(data['password']),
                    first_name=data['first_name'] if data.get('first_name') else None,
                    last_name=data['last_name'] if data.get('last_name') else None,
            )
        except IntegrityError:
            data = {'message': 'User already registered!'}
            return Response(data, status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET', 'PUT', 'DELETE'))
@permission_classes((IsAuthenticated,))
def profile_handler(request: HttpRequest) -> Response:
    user = request.user

    try:
        profile = user.profile
    except AttributeError:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
