
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Target, Subdomain, IP, CIDR, ASN, Vulnerability, Site
from .serializers import TargetSerializer, SubdomainSerializer, IPSerializer, CIDRSerializer, ASNSerializer, VulnerabilitySerializer, SiteSerializer
from django.http import JsonResponse


class TargetViewSet(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [AllowAny]

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

    # @action(detail=False, methods=['get'])
    # def target_subdomains(self, request, pk=None):
    #     address = request.query_params.get('address')
    #     target = Target.objects.filter(address=address).first()
    #     if target is None:target = Site.objects.filter(address=address).first()
    #     if target is None:
    #         return Response({'error': 'No target found with the given address'}, status=404)
    #     serializer = SubdomainSerializer(target.subdomains, many=True)
    #     return Response(serializer.data)

    # @action(detail=False, methods=['get'])
    # def target_details(self, request, pk=None):
    #     address = request.query_params.get('address')
    #     target = Target.objects.filter(address=address).first()
    #     if target is None:target = Site.objects.filter(address=address).first()
    #     if target is None:
    #         return Response({'error': 'No target found with the given address'}, status=404)
    #     serializer = TargetSerializer(target)
    #     return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        address = request.data.get('address')
        target, created = Target.objects.get_or_create(address=address)

        if 'name' in request.data:
            target.name = request.data.get('name')

        if 'behind_cdn' in request.data:
            target.behind_cdn = request.data.get('behind_cdn')

        # Get or create subdomains
        if 'subdomains' in request.data:
            target.subdomains.clear()
            subdomains_data = request.data.get('subdomains', [])
            for subdomain_data in subdomains_data:
                subdomain, created = Subdomain.objects.get_or_create(address=subdomain_data)
                target.subdomains.add(subdomain)

        # Get or create IPs
        if 'ips' in request.data:
            target.ips.clear()
            ips_data = request.data.get('ips', [])
            for ip_data in ips_data:
                ip, created = IP.objects.get_or_create(ip=ip_data)
                target.ips.add(ip)

        # Get or create CIDRs
        if 'cidrs' in request.data:
            target.cidrs.clear()
            cidrs_data = request.data.get('cidrs', [])
            for cidr_data in cidrs_data:
                cidr, created = CIDR.objects.get_or_create(ip=cidr_data)
                target.cidrs.add(cidr)

        # Get or create ASNs
        if 'asns' in request.data:
            target.asns.clear()
            asns_data = request.data.get('asns', [])
            for asn_data in asns_data:
                asn, created = ASN.objects.get_or_create(ip=asn_data)
                target.asns.add(asn)

        # Get or create vulnerabilities
        if 'vulnerabilities' in request.data:
            target.vulnerabilities.clear()
            vulnerabilities_data = request.data.get('vulnerabilities', [])
            for vulnerability_data in vulnerabilities_data:
                vulnerability, created = Vulnerability.objects.get_or_create(
                    name=vulnerability_data.get('name'),
                    attack_vector=vulnerability_data.get('attack_vector'),
                    description=vulnerability_data.get('description'),
                    cvss=vulnerability_data.get('cvss'),
                    write_up=vulnerability_data.get('write_up'),
                    report=vulnerability_data.get('report')
                )
                target.vulnerabilities.add(vulnerability)
        
        target.save()
        serializer = self.get_serializer(target)
        return Response(serializer.data)
    @action(detail=False, methods=['put'])
    def update_target(self, request, pk=None):
        address = request.data.get('address')
        target = Target.objects.filter(address=address).first()
        if target is None:
            return Response({'error': 'No target found with the given address'}, status=404)
        
        # Get or create subdomains
        subdomains_data = request.data.get('subdomains', [])
        for subdomain_data in subdomains_data:
            subdomain, created = Subdomain.objects.get_or_create(address=subdomain_data)
            target.subdomains.add(subdomain)

        # Get or create IPs
        ips_data = request.data.get('ips', [])
        for ip_data in ips_data:
            ip, created = IP.objects.get_or_create(ip=ip_data)
            target.ips.add(ip)

        # Get or create CIDRs
        cidrs_data = request.data.get('cidrs', [])
        for cidr_data in cidrs_data:
            cidr, created = CIDR.objects.get_or_create(ip=cidr_data)
            target.cidrs.add(cidr)

        # Get or create ASNs
        asns_data = request.data.get('asns', [])
        for asn_data in asns_data:
            asn, created = ASN.objects.get_or_create(ip=asn_data)
            target.asns.add(asn)

        # Get or create vulnerabilities
        vulnerabilities_data = request.data.get('vulnerabilities', [])
        for vulnerability_data in vulnerabilities_data:
            vulnerability, created = Vulnerability.objects.get_or_create(
                name=vulnerability_data.get('name'),
                attack_vector=vulnerability_data.get('attack_vector'),
                description=vulnerability_data.get('description'),
                cvss=vulnerability_data.get('cvss'),
                write_up=vulnerability_data.get('write_up'),
                report=vulnerability_data.get('report')
            )
            target.vulnerabilities.add(vulnerability)
        
        serializer = TargetSerializer(target, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        


    # @action(detail=True, methods=['get', 'put'])
    # def target_details(self, request, pk=None):
    #     target = self.get_object()
    #     if request.method == 'GET':

    #         address = request.GET.get('address')
    #         target = Target.objects.filter(address=address).first()
    #         if target is None:
    #             return Response({'error': 'No target found with the given address'}, status=404)
    #         serializer = TargetSerializer(target)
    #         if serializer.is_valid():
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=400)
    #     elif request.method == 'PUT':
    #         serializer = TargetSerializer(target, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=400)

    # @action(detail=True, methods=['post'])
    # def add_vulnerability(self, request, pk=None):
    #     target = self.get_object()
    #     serializer = VulnerabilitySerializer(data=request.data)
    #     if serializer.is_valid():
    #         vulnerability = serializer.save()
    #         target.vulnerabilities.add(vulnerability)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)


