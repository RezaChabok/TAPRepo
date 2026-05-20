
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
    cvss = serializers.DecimalField(max_digits=3, decimal_places=1, 
                                    allow_null=True, required=False)
    report = serializers.URLField(allow_null=True, required=False)

    class Meta:
        model = Vulnerability
        fields = ['name', 'attack_vector', 'description', 'cvss', 'write_up', 'report']
        extra_kwargs = {
            'description': {'required': False, 'allow_null': True},
            'write_up': {'required': False, 'allow_null': True},
        }


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