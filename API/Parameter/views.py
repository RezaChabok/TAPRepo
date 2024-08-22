
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Parameter, Type, Site
from .serializers import ParameterSerializer, TypeSerializer
import json

from rest_framework.exceptions import ValidationError

def validate_top(top):
    try:
        top = int(top)
        return top
    except:
        raise ValidationError("The 'top' parameter must be an integer.")

def validate_type(name):
    type = Type.objects.filter(name = name).first()
    if type is None:raise ValidationError("The 'type' does not exist..")

class ParameterViewSet(viewsets.ModelViewSet):
    """Get All Parameters

    Args:
        viewsets (Parameter): All useful parameter used in requests.

    Returns:
        Parameters: Al Parameters saved in DB.
    """
    
    
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        params = request.data.get('params')
        if params:
            for param in params:
                name = param['name']
                parameter, created = Parameter.objects.get_or_create(name=name)

                if 'site' in request.data:
                    site, created = Site.objects.get_or_create(address=request.data.get('site'))
                    parameter.site.add(site)
                
                if request.data.get('type') is not None:
                    type, created = Type.objects.get_or_create(name=request.data.get('type'))
                    parameter.type.add(type)
                
                parameter.save()
            # serializer = self.get_serializer(parameter)
            return Response({'done':'done'})
            
        name = request.data.get('name')
        parameter, created = Parameter.objects.get_or_create(name=name)

        if 'site' in request.data:
            site, created = Site.objects.get_or_create(address=request.data.get('site'))
            parameter.site.add(site)
        
        if request.data.get('type') is not None:
            type, created = Type.objects.get_or_create(name=request.data.get('type'))
            parameter.type.add(type)
        
        parameter.save()
        serializer = self.get_serializer(parameter)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_top(self, request):
        top = request.query_params.get('top')
        top = validate_top(top)
        parameters = Parameter.get_rank(top=top)
        serializer = ParameterSerializer(parameters, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_by_type(self, request):
        type_name = request.query_params.get('type')
        validate_type(type_name)
        parameters = Parameter.get_by_type(type_name=type_name)
        serializer = ParameterSerializer(parameters, many=True)
        return Response(serializer.data)

    