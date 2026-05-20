
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Parameter, Type, ParameterSite
from .serializers import ParameterSerializer, TypeSerializer, QuerysetListSerializer
import json
from django.db.models import Count
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
    queryset = Parameter.objects.annotate(site_count=Count('site'))
    serializer_class = ParameterSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        site = request.query_params.get('site')
        type_name = request.query_params.get('type')
        top = request.query_params.get('top')

        if site:
            queryset = queryset.filter(site__address=site)
        if type_name:
            queryset = queryset.filter(type__name=type_name)
        if top:
            queryset = queryset.order_by('-site_count')[:int(top)]

        names = queryset.values_list('name', flat=True)
        return Response(names)

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
            return Response({'done':'done'})
            
        name = request.data.get('name')
        parameter, created = Parameter.objects.get_or_create(name=name)

        if 'site' in request.data:
            site, created = ParameterSite.objects.get_or_create(address=request.data.get('site'))
            parameter.site.add(site)
        
        if request.data.get('type') is not None:
            type, created = Type.objects.get_or_create(name=request.data.get('type'))
            parameter.type.add(type)
        
        parameter.save()
        serializer = self.get_serializer(parameter)
        return Response(serializer.data)