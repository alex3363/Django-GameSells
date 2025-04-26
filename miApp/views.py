from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse 
import requests 
from requests.exceptions import HTTPError 
from django.views.generic import View



def registrarsejg(request):
    if request.method == 'GET':
        return render(request, 'registrarsejg.html', {'form': UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'registrarsejg.html', {"form": UserCreationForm, "error": "Username already exists."})
    return render(request, 'registrarsejg.html', {"form": UserCreationForm, "error": "Passwords did not match."})
        

def carrito_compra(request):
    context = {"carro":request.session.get("carro", [])}
    user = request.user
    return render(request, 'miApp/carrito_compra.html',  context)

def dropitem(request, codigo):
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            if item[4] > 1:
                item[4] -= 1
                item[5] = item[3] * item[4]
                break
            else:
                carro.remove(item)
    request.session["carro"] = carro
    return redirect(to="carrito_compra")

def addtocar(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    carro = request.session.get("carro", [])

    tipo_vista_mapping = {
        1: 'accion',
        2: 'aventura',
        3: 'rpg',
        4: 'shooters',
        5: 'terror'
    }

    for item in carro:
        if item[0] == codigo and producto.stock > item[4]:
            item[4] += 1
            item[5] = item[3] * item[4]
            print('1')
            break
        elif item[0] == codigo and producto.stock <= item[4]:
            if producto.tipo in tipo_vista_mapping:
                return redirect(to=tipo_vista_mapping[producto.tipo])
    else:
        carro.append([codigo, producto.detalle, producto.imagen, producto.precio, 1, producto.precio])
        print('2')

    request.session["carro"] = carro
    if producto.tipo in tipo_vista_mapping:
        return redirect(to=tipo_vista_mapping[producto.tipo])





def signout(request):
    logout(request)
    return redirect('index')



   
def inicio_sesionjg(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesionjg.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inicio_sesionjg.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('index')
    
def micuenta(request):
    user = request.user  # Obtener el usuario actual

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)  # Pasar el usuario actual al formulario
        if form.is_valid():
            # Actualizar el correo electrónico solo si se proporciona en el formulario
            if 'email' in form.cleaned_data:
                user.email = form.cleaned_data['email']
                user.save()  # Guardar los cambios en el usuario
            return redirect(to="index")
    else:
        form = CustomUserChangeForm(instance=user)  # Pasar el usuario actual al formulario en caso de GET request
    
    return render(request, 'micuentatf.html', {'form': form, 'user': user})



def accion(request):
    accion = Producto.objects.all()
    return render(request, 'accion.html', {'accion': accion})

def informes_creados(request):
    informes_creados = micuentatf.objects.all()
    return render(request, 'informes_creados.html', {"informes_creados": informes_creados})

def terror(request):
      terror = Producto.objects.all()
      return render(request, 'terror.html', {'terror': terror})

def shooters(request):
      shooters = Producto.objects.all() 
      return render(request, 'shooters.html', {'shooters': shooters})

def aventura(request):
    aventura = Producto.objects.all()
    return render(request, 'aventura.html', {'aventura': aventura})

def rpg(request):
      rpg = Producto.objects.all()
      return render(request, 'rpg.html', {'rpg': rpg})


def listado(request):
      listado = Producto.objects.all()
      return render(request, 'listado.html', {'listado': listado})


def listado(request):
    # Generar una lista de números del 1 al 20
    page_numbers = list(range(1, 21))
    return render(request, 'listado.html', {'page_numbers': page_numbers})

def index(request):
    return render(request, 'index.html')

def videos_view(request):
    return render (request, 'videos.html')


# para que funcione la conexion con la api de gamespot
def proxy_to_api(request):
    api_key = 'fed2b26e280a9f34b5a93d9dbb3d2677c446d2ed'
    page_size = 25  # o el valor que necesites
    page = request.GET.get('page', 1)
    url = f'http://www.gamespot.com/api/videos/?api_key={api_key}&format=json&limit={page_size}&sort=publish_date:desc&page={page}'
    
    headers = {
        'User-Agent': 'MiApp/1.0 (miemail@example.com)'  
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            return JsonResponse(data)
        except ValueError:  # incluye JSONDecodeError
            return JsonResponse({'error': 'La respuesta no es un JSON válido'}, status=500)
    else:
        return JsonResponse({'error': 'Error en la solicitud a la API'}, status=response.status_code)



def recuperarcontra(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Si el usuario y el correo electrónico son correctos, redireccionar a la página de cambio de contraseña
                return redirect('cambiar_contra', user_id=user.id)
            except User.DoesNotExist:
                # Si el usuario o el correo electrónico no son correctos, se muestra un mensaje de error
                messages.error(request, "El usuario o correo electrónico no son correctos.")
    else:
        form = PasswordResetForm()
    
    return render(request, 'recuperarcontra.html', {'form': form})

def cambiar_contra(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Contraseña cambiada correctamente. Ahora puedes iniciar sesión.")
            return redirect('index')  # Redireccionar al usuario a la página de inicio
    else:
        form = ChangePasswordForm()
    
    return render(request, 'cambiar_contra.html', {'form': form}) 

