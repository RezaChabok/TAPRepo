from django.contrib import admin

# Register your models here.
from .models import Parameter, Type, Site
admin.site.register(Parameter)
admin.site.register(Type)
admin.site.register(Site)