from django.urls import path, include 
from . import views
#api 
from rest_framework import routers


router=routers.DefaultRouter()
router.register(r'micuentatf',views.micuentatfViewset)
router.register(r'Producto',views.ProductoViewset)

urlpatterns = [ 
    path('', include(router.urls)),           
    path('productos/', views.lista_productos, name= 'lista_productos'),
    path('productos/<id>/', views.vista_producto, name='vista_producto'),
    
]