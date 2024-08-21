from django.contrib import admin

from .models import Target, Subdomain, IP, CIDR, ASN, Vulnerability, Site
admin.site.register(Target)
admin.site.register(Site)
admin.site.register(Subdomain)
admin.site.register(IP)
admin.site.register(CIDR)
admin.site.register(ASN)
admin.site.register(Vulnerability)