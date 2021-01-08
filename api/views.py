
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import TaskSerializer, RegistrationSerializer
from .models import Task
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST'])
def apiRegistration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'Successfully registered a new user.'
        data['email'] = user.email
        data['username'] = user.username
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/'
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def taskList(request):
    tasks = request.user.task_set.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def detailList(request, pk):
    user = request.user
    task = user.task_set.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createList(request):
    user = request.user
    task = Task(user=user)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def updateList(request, pk):
    user = request.user
    task = user.task_set.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def deleteList(request, pk):
    user = request.user
    task = user.task_set.get(id=pk)
    task.delete()
    return Response('Task successfully deleted!')