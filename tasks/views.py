from django.shortcuts import render

# Create your views here.
# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
# API definition for task
from .serializers import TaskSerializer
# Task model
from .models import Task


@csrf_exempt
def tasks(request):

    '''
    List all task snippets
    '''
    if(request.method == 'GET'):
        # get all the tasks

        tasks = Task.objects.all()
        # serialize the task data
        serializer = TaskSerializer(tasks, many=True)
        # return a Json response
        # import ipdb; ipdb.set_trace()
        # dictionary = serializer.data
        # list_of_data=[]
        # for dict1 in dictionary:
        #     list_of_data.append(dict(dict1))
        # print(list_of_data)
        return JsonResponse(serializer.data,safe=False)
    elif(request.method == 'POST'):
        # parse the incoming information
        data = JSONParser().parse(request)
        # instanciate with the serializer
        serializer = TaskSerializer(data=data)
        # check if the sent information is okay

        if(serializer.is_valid()):
            # if okay, save it on the database
            serializer.save()
            # provide a Json Response with the data that was saved
            return JsonResponse(serializer.data, status=201)
            # provide a Json Response with the necessary error information
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def task_detail(request,id):
    print("-----0",request.method)
    try:
        # obtain the task with the passed id.
        task = Task.objects.get(pk=id)
    except:
        # respond with a 404 error message
        return HttpResponse(status=404)
    
    if (request.method =='GET'):
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)
        
    if(request.method == 'PUT'):
        # parse the incoming information
        data = JSONParser().parse(request)
        # instanciate with the serializer
        serializer = TaskSerializer(task, data=data)
        # check whether the sent information is okay
        if(serializer.is_valid()):  
            # if okay, save it on the database
            serializer.save() 
            # provide a JSON response with the data that was submitted
            return JsonResponse(serializer.data, status=201)
        # provide a JSON response with the necessary error information
        return JsonResponse(serializer.errors, status=400)
    if (request.method == 'DELETE'):
        # import ipdb; ipdb.set_trace()
        # delete the task
        task.delete() 
        # return a no content response.
        return HttpResponse(status=204) 