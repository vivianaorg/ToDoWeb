from django.shortcuts import render
from .models import Task, Category
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter
from .serializers import  TaskSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model

def tareaJson(request):
    tareas_data = list(Task.objects.values())
    return JsonResponse(tareas_data, safe=False)

def listaJson(request):
    tareas = Task.objects.order_by("-priority").values()
    lista_tareas = list(tareas)
    return JsonResponse(lista_tareas, safe=False)

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "ToDoApp/task_list.html", {"tasks": tasks})
'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
'''
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends=[OrderingFilter]
    ordering_fields=['priority']
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return self.request.user.tasks.all()

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
'''
@csrf_exempt
def ToDoApp_list(request):
    if request.method == 'GET':
        snippets = Task.objects.all()
        serializer = TaskSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def ToDoApp_detail(request, pk):
    try:
        snippet = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
'''    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

