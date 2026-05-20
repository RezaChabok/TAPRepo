from django.db import models
from django.core.exceptions import ValidationError
import re
from django.core.validators import MinValueValidator, MaxValueValidator

class Subdomain(models.Model):
    address = models.TextField()

    def __str__(self):
        return f"{self.address}"

class IP(models.Model):
    ip = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return f"{self.ip}"

def validate_cidr(value):
    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$')
    if not pattern.match(value):
        raise ValidationError("Enter a valid CIDR notation (e.g., 192.168.1.0/24)")

class CIDR(models.Model):
    ip = models.CharField(max_length=20, unique=True, validators=[validate_cidr])

    def __str__(self):
        return f"{self.ip}"


class ASN(models.Model):
    ip = models.TextField()

    def __str__(self):
        return f"{self.ip}"



class Vulnerability(models.Model):
    name = models.CharField(max_length=255)
    attack_vector = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cvss = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    write_up = models.TextField(null=True, blank=True)
    report = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = [['name', 'attack_vector']]

    def __str__(self):
        return f"{self.name}"


class AbstractBaseModel(models.Model):
    address = models.TextField(null=True,blank=True, unique=True)
    name = models.TextField(null=True,blank=True)
    subdomains = models.ManyToManyField(Subdomain, blank=True)
    ips = models.ManyToManyField(IP, blank=True)
    cidrs = models.ManyToManyField(CIDR, blank=True)
    asns = models.ManyToManyField(ASN, blank=True)
    behind_cdn = models.BooleanField(null=True,blank=True)
    vulnerabilities = models.ManyToManyField(Vulnerability, blank=True)

    class Meta:
        abstract = True

    def add_related_items(self, field_name, data_list, model_class, field_key='address'):
        if not data_list:
            return

        related_manager = getattr(self, field_name)
        related_manager.clear()

        for item in data_list:
            kwargs = {field_key: item}
            obj, created = model_class.objects.get_or_create(**kwargs)
            related_manager.add(obj)

    def add_vulnerabilities(self, vulnerabilities_data):
        if not vulnerabilities_data:
            return

        self.vulnerabilities.clear()
        for vuln_data in vulnerabilities_data:
            name = vuln_data.get('name')
            attack_vector = vuln_data.get('attack_vector')
            if not name or not attack_vector:
                continue

            vulnerability, created = Vulnerability.objects.get_or_create(
                name=name,
                attack_vector=attack_vector,
                defaults={
                    'description': vuln_data.get('description', ''),
                    'cvss': vuln_data.get('cvss'),
                    'write_up': vuln_data.get('write_up', ''),
                    'report': vuln_data.get('report', ''),
                }
            )

            if not created:
                vulnerability.description = vuln_data.get('description', vulnerability.description)
                vulnerability.cvss = vuln_data.get('cvss', vulnerability.cvss)
                vulnerability.write_up = vuln_data.get('write_up', vulnerability.write_up)
                vulnerability.report = vuln_data.get('report', vulnerability.report)
                vulnerability.save()

            self.vulnerabilities.add(vulnerability)


class Site(AbstractBaseModel):
    pass


class Target(AbstractBaseModel):
    SubSite = models.ManyToManyField(Site, blank=True)
