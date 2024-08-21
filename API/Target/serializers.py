
from rest_framework import serializers
from .models import Target, Subdomain, IP, CIDR, ASN, Vulnerability, Site

class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        exclude = ('id', )

class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ['ip']

class CIDRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CIDR
        fields = ['name']

class ASNSerializer(serializers.ModelSerializer):
    class Meta:
        model = ASN
        fields = ['name']

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['name']

class SiteSerializer(serializers.ModelSerializer):
    subdomains = SubdomainSerializer(many=True, read_only=True)
    ips = IPSerializer(many=True, read_only=True)
    cidrs = CIDRSerializer(many=True, read_only=True)
    asns = ASNSerializer(many=True, read_only=True)
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ['address', 'name', 'subdomains', 'ips', 'cidrs', 'asns', 'behind_cdn', 'vulnerabilities']


class TargetSerializer(serializers.ModelSerializer):
    subdomains = SubdomainSerializer(many=True, read_only=True)
    ips = IPSerializer(many=True, read_only=True)
    cidrs = CIDRSerializer(many=True, read_only=True)
    asns = ASNSerializer(many=True, read_only=True)
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    SubSite = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Target
        fields = ['address', 'name', 'SubSite', 'subdomains', 'ips', 'cidrs', 'asns', 'behind_cdn', 'vulnerabilities']
    
    # def create(self, validated_data):
    #     # Extract fields from validated_data
    #     address = validated_data.pop('address')
    #     name = validated_data.pop('name', None)
    #     subdomains = validated_data.pop('subdomains', [])
    #     ips = validated_data.pop('ips', [])
    #     cidrs = validated_data.pop('cidrs', [])
    #     asns = validated_data.pop('asns', [])
    #     behind_cdn = validated_data.pop('behind_cdn', None)
    #     vulnerabilities = validated_data.pop('vulnerabilities', [])

    #     # Create the new target
    #     target = Target.objects.create(address=address, name=name, behind_cdn=behind_cdn)

    #     # Add the many-to-many fields
    #     for subdomain in subdomains:
    #         target.subdomains.add(subdomain)
    #     for ip in ips:
    #         target.ips.add(ip)
    #     for cidr in cidrs:
    #         target.cidrs.add(cidr)
    #     for asn in asns:
    #         target.asns.add(asn)
    #     for vulnerability in vulnerabilities:
    #         target.vulnerabilities.add(vulnerability)

    #     return target