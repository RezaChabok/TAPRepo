
from rest_framework import serializers
from .models import Parameter, Type, Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['address']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']


class ParameterSerializer(serializers.ModelSerializer):
    site = SiteSerializer(many=True, read_only=True)
    type = TypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Parameter
        fields = ['name', 'type', 'site', 'count']

    # def create(self, validated_data):
    #     type_data = validated_data.pop('type')
    #     parameter, created = Parameter.objects.get_or_create(**validated_data)
    #     # if not created:
    #     #     parameter.count += 1
    #     for type_name in type_data:
    #         type, _ = Type.objects.get_or_create(name=type_name)
    #         parameter.type.add(type)
    #     parameter.save()
    #     return parameter
