from miApp import views
from django.urls import path
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from .views import proxy_to_api

from django.views.generic.base import RedirectView

urlpatterns = [
    path('logout/', views.signout, name='logout'),
    path('logout', RedirectView.as_view(url='/logout/')), 
    path('terror/', views.terror, name='terror'),   
    path('inicio_sesionjg/', views.inicio_sesionjg, name='inicio_sesionjg'),
    path('', views.index, name='index'),
    path('micuenta/', views.micuenta, name='micuenta'),
    path('informes_creados/', views.informes_creados, name='informes_creados'),
    path('recuperarcontra/', views.recuperarcontra, name='recuperarcontra'),
    path('registrarsejg/', views.registrarsejg, name='registrarsejg'), 
    path('accion/', views.accion, name='accion'),
    path('shooters/', views.shooters, name='shooters'),
    path('aventura/', views.aventura, name='aventura'),
    path('addtocar/<codigo>', views.addtocar, name="addtocar"),
    path('rpg/', views.rpg, name='rpg'),
    path('dropitem/<codigo>', views.dropitem, name="dropitem"),
    path('carrito_compra', views.carrito_compra, name="carrito_compra"),
    path('cambiar_contra/<int:user_id>/', views.cambiar_contra, name='cambiar_contra'),
    path('listado/', views.listado, name='listado'),
    path('videos/', views.videos_view, name='videos'),
    path('api/proxy', proxy_to_api, name='proxy_to_api'),

]   
