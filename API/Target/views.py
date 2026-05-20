
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Target, Subdomain, IP, CIDR, ASN, Vulnerability, Site
from .serializers import TargetSerializer, SubdomainSerializer, IPSerializer, CIDRSerializer, ASNSerializer, VulnerabilitySerializer, SiteSerializer
from django.http import JsonResponse

class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        address = self.request.query_params.get('address')
        if address is None: return Target.objects.all()
        target = Target.objects.filter(address=address)
        if len(target) == 0:
            target = Site.objects.filter(address=address)  
        if target is None:
            return Response({'error': 'No target found with the given address'}, status=404)              
        return target
        
    @action(detail=False, methods=['get'])
    def all_subdomains(self, request):
        subdomains = Subdomain.objects.all()
        serializer = SubdomainSerializer(subdomains, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        address = request.data.get('address')
        target, created = Target.objects.get_or_create(address=address)

        if 'name' in request.data:
            target.name = request.data.get('name')
        if 'behind_cdn' in request.data:
            target.behind_cdn = request.data.get('behind_cdn')

        target.add_related_items('subdomains', request.data.get('subdomains'), Subdomain)
        target.add_related_items('ips', request.data.get('ips'), IP, field_key='ip')
        target.add_related_items('cidrs', request.data.get('cidrs'), CIDR, field_key='ip')
        target.add_related_items('asns', request.data.get('asns'), ASN, field_key='ip')
        target.add_vulnerabilities(request.data.get('vulnerabilities'))

        target.save()
        serializer = self.get_serializer(target)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_target(self, request, pk=None):
        address = request.data.get('address')
        target = Target.objects.filter(address=address).first()
        if target is None:
            return Response({'error': 'No target found with the given address'}, status=404)

        target.add_related_items('subdomains', request.data.get('subdomains'), Subdomain)
        target.add_related_items('ips', request.data.get('ips'), IP, field_key='ip')
        target.add_related_items('cidrs', request.data.get('cidrs'), CIDR, field_key='ip')
        target.add_related_items('asns', request.data.get('asns'), ASN, field_key='ip')
        target.add_vulnerabilities(request.data.get('vulnerabilities'))

        target.save()
        serializer = TargetSerializer(target)
        return Response(serializer.data)