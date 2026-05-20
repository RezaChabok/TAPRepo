from django.db import models

class Type(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return f"{self.name}"


class ParameterSite(models.Model):
    address = models.TextField(unique=True)
    def __str__(self):
        return f"{self.address}"


class Parameter(models.Model):
    class Meta:
        ordering = []

    name = models.TextField(unique=True)
    type = models.ManyToManyField(Type, blank=True)
    site = models.ManyToManyField(ParameterSite, blank=True)

    @property
    def count(self):
        return self.site.count()

    def __str__(self):
        return self.name

    @staticmethod
    def get_rank(top: int):
        
        if isinstance(top, int):return Parameter.objects.all()[:top]
        return "Enter integer number!!!"
    
    @staticmethod
    def get_by_type(type_name: str):
        type_obj = Type.objects.filter(name=type_name).first()
        return Parameter.objects.filter(type=type_obj)