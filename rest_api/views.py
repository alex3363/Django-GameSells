from django.shortcuts import render

from rest_framework import status, viewsets 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from django.shortcuts import get_object_or_404
from miApp.models import *
from .serializers import ProductoSerializer
from .serializers import micuentatfSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def lista_productos(request):
    if request.method == 'GET':
        producto = Producto.objects.all()
        serializer = ProductoSerializer(producto, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)  # Utiliza request.data en lugar de JSONParser

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticated,))
def vista_producto(request, id):
    try:
        producto = Producto.objects.get(codigo=id)  # Cambio aquí de 'codigo' a 'id'
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data) 
    
    elif request.method == 'PUT' or request.method == 'PATCH' : 
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    elif request.method == 'DELETE': 
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class micuentatfViewset(viewsets.ModelViewSet):
    queryset = micuentatf.objects.all()
    serializer_class = micuentatfSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Asigna el usuario actual como propietario de la cuenta

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  
    

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 