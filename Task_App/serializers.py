from rest_framework import serializers
from django.contrib.auth.models import User
from Task_App.models import TaskDb

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:

        password = serializers.CharField(write_only =True)
        model = User
        fields =["username","email","password"]
        read_only_fields  =["id"]
    def create(self,validated_data):
        user = User.objects.create_user(
                username= validated_data["username"],
                email=validated_data["email"],
                password = validated_data["password"]
        )
        return user
    
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskDb
        fields = "__all__"
        read_only_fields =["id","user"]