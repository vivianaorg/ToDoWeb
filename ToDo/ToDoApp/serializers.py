from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task,Category

'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']
'''

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField(required = False, allow_blank=True, max_length= 200)
    completed = serializers.BooleanField(required = False)
    priority = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = (
            "id",
            "category",
            "name",
            "description",
            "fecha_inicio",
            "fecha_final",
            "completed",
            "priority",
        )
        
    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.name= validated_data.get('name', instance.name)
        instance.description= validated_data.get('description', instance.description)
        instance.completed= validated_data.get('completed', instance.completed)
        instance.priority= validated_data.get('priority', instance.priority)
        instance.save()
        return instance