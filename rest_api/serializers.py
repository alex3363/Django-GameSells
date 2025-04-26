from rest_framework import serializers
from miApp.models import Producto 
from miApp.models import micuentatf 

class ProductoSerializer(serializers.ModelSerializer):
     class Meta: 
          model = Producto
          fields =['codigo','detalle','precio','stock','oferta', 'imagen', 'tipo'] 

class micuentatfSerializer(serializers.ModelSerializer):
     class Meta: 
          model = micuentatf
          fields =['title','description','created','datecompleted', 'important', 'user'] 
          
          
          
          
          

