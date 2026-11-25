from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from Task_App.serializers import RegistrationSerializer,TaskSerializer
from Task_App.models import TaskDb
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegistrationView(APIView):

    def post(self,request):

        form_data = request.data
        serializer_instance = RegistrationSerializer(data=form_data)
        serializer_instance.is_valid()
        serializer_instance.save()
        return Response(data= {
            "Message" :"Registration Succesfull..!",
            "Data" :serializer_instance.data})
    
class TaskListCreateView(APIView):

    permission_classes =[IsAuthenticated]

    def get(self,request):

        qs = TaskDb.objects.filter(user = request.user)

        serializer_instance = TaskSerializer(qs,many=True)
        return Response( data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = TaskSerializer(data= form_data)

        if serializer_instance.is_valid():
            serializer_instance.save(user = request.user)

            return Response(data= {
                "Message": "Data Added Succesfully..!",
                "Details": serializer_instance.data
            })
        else:
            return Response(data= serializer_instance.errors)

class TaskUpdateRetrieveDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,pk):

        qs = TaskDb.objects.filter(user = request.user)

        serializer_instance = TaskSerializer(qs,many=True)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def put(self,request,pk):

        task_object = get_object_or_404(TaskDb,id=pk)

        if task_object.user != request.user:
            raise serializers.ValidationError("only owners can update data..")
        else:

            form_data = request.data
            serializer_instance = TaskSerializer(data = form_data,instance = task_object)

            if serializer_instance.is_valid():
                serializer_instance.save()

                return Response(data={
                    "message" : "Updated Succesfully..!",
                    "data" :serializer_instance.data
                })
            else:
                return Response(data=serializer_instance.errors)

    def delete(self,request,pk):

        task_object = get_object_or_404(TaskDb,id=pk,user=request.user)

        task_object.delete()
        return Response(data= {
            "Message" : "Deletion Succesfull..!!"
        })

class LogoutView(APIView):

    def post(self,request):

        request.user.authtoken.delete()

        return Response(data={
            "Message" : "Token Deleted Succesfully..!!"
        })


        