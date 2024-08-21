from django.db import models

class Subdomain(models.Model):
    address = models.TextField()

    def __str__(self):
        return f"{self.address}"

class IP(models.Model):
    ip = models.TextField()

    def __str__(self):
        return f"{self.ip}"

class CIDR(models.Model):
    ip = models.TextField()

    def __str__(self):
        return f"{self.ip}"

class ASN(models.Model):
    ip = models.TextField()

    def __str__(self):
        return f"{self.ip}"

class Vulnerability(models.Model):
    name = models.TextField(null=True,blank=True)
    attack_vector = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    cvss = models.TextField(null=True,blank=True)
    write_up = models.TextField(null=True,blank=True)
    report = models.TextField(null=True,blank=True)

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

    def __str__(self):
        return f"{self.address}"


class Site(AbstractBaseModel):
    pass


class Target(AbstractBaseModel):
    SubSite = models.ManyToManyField(Site, blank=True)
