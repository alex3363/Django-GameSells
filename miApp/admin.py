from django.contrib import admin
from .models import *

class MicuentaAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )
  
admin.site.register(micuentatf,MicuentaAdmin)
admin.site.register(Producto)
