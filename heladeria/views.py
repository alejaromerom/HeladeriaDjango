from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from datetime import datetime
from .models import Usuario, Ingrediente, Producto, Venta
from .forms import RegistroForm, IngredienteForm, ProductoForm, VentaForm


# Funciones auxiliares para verificar roles
def es_administrador(user):
    return user.is_authenticated and user.rol == 'ADMINISTRADOR'

def es_empleado(user):
    return user.is_authenticated and user.rol in ['EMPLEADO', 'ADMINISTRADOR']

def es_cliente(user):
    return user.is_authenticated and user.rol in ['CLIENTE', 'EMPLEADO', 'ADMINISTRADOR']


# ===== VISTAS PÚBLICAS (sin autenticación) =====

def home(request):
    """Página principal - Lista de productos (acceso público)"""
    productos = Producto.objects.all()
    return render(request, 'heladeria/home.html', {'productos': productos})


def login_view(request):
    """Vista de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'heladeria/login.html')


def registro_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'heladeria/registro.html', {'form': form})


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('home')


# ===== VISTAS AUTENTICADAS =====

@login_required
def dashboard(request):
    """Dashboard principal según el rol del usuario"""
    context = {
        'usuario': request.user,
        'total_productos': Producto.objects.count(),
        'total_ingredientes': Ingrediente.objects.count(),
    }
    
    # Si es administrador, mostrar estadísticas adicionales
    if es_administrador(request.user):
        context['total_ventas_hoy'] = Venta.objects.filter(
            fecha__date=timezone.now().date()
        ).aggregate(total=Sum('total'))['total'] or 0
        
        context['ventas_hoy'] = Venta.objects.filter(
            fecha__date=timezone.now().date()
        ).count()
    
    return render(request, 'heladeria/dashboard.html', context)


# ===== VISTAS DE PRODUCTOS =====

def producto_lista(request):
    """Lista de productos con información (acceso público)"""
    productos = Producto.objects.all()
    productos_info = []
    
    for producto in productos:
        productos_info.append({
            'producto': producto,
            'costo': producto.calcular_costo(),
            'calorias': producto.calcular_calorias(),
            'rentabilidad': producto.calcular_rentabilidad(),
            'hay_stock': producto.hay_inventario_disponible()
        })
    
    return render(request, 'heladeria/producto_lista.html', {'productos_info': productos_info})


def producto_detalle(request, pk):
    """Detalle de un producto específico"""
    producto = get_object_or_404(Producto, pk=pk)
    context = {
        'producto': producto,
        'costo': producto.calcular_costo(),
        'calorias': producto.calcular_calorias(),
        'rentabilidad': producto.calcular_rentabilidad(),
        'ingredientes': producto.ingredientes.all(),
        'hay_stock': producto.hay_inventario_disponible()
    }
    return render(request, 'heladeria/producto_detalle.html', context)


@login_required
@user_passes_test(es_empleado)
def producto_crear(request):
    """Crear nuevo producto (solo empleados y admin)"""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            # Agregar los ingredientes seleccionados
            form.save_m2m()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('producto_lista')
    else:
        form = ProductoForm()
    
    return render(request, 'heladeria/producto_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@user_passes_test(es_empleado)
def producto_editar(request, pk):
    """Editar producto existente (solo empleados y admin)"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('producto_lista')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'heladeria/producto_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@user_passes_test(es_empleado)
def producto_eliminar(request, pk):
    """Eliminar producto (solo empleados y admin)"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('producto_lista')
    
    return render(request, 'heladeria/producto_eliminar.html', {'producto': producto})


# ===== VISTAS DE INGREDIENTES =====

@login_required
@user_passes_test(es_empleado)
def ingrediente_lista(request):
    """Lista de ingredientes (solo empleados y admin)"""
    ingredientes = Ingrediente.objects.all()
    return render(request, 'heladeria/ingrediente_lista.html', {'ingredientes': ingredientes})


@login_required
@user_passes_test(es_empleado)
def ingrediente_crear(request):
    """Crear nuevo ingrediente (solo empleados y admin)"""
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente creado exitosamente.')
            return redirect('ingrediente_lista')
    else:
        form = IngredienteForm()
    
    return render(request, 'heladeria/ingrediente_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@user_passes_test(es_empleado)
def ingrediente_editar(request, pk):
    """Editar ingrediente existente (solo empleados y admin)"""
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente actualizado exitosamente.')
            return redirect('ingrediente_lista')
    else:
        form = IngredienteForm(instance=ingrediente)
    
    return render(request, 'heladeria/ingrediente_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@user_passes_test(es_empleado)
def ingrediente_eliminar(request, pk):
    """Eliminar ingrediente (solo empleados y admin)"""
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    
    if request.method == 'POST':
        ingrediente.delete()
        messages.success(request, 'Ingrediente eliminado exitosamente.')
        return redirect('ingrediente_lista')
    
    return render(request, 'heladeria/ingrediente_eliminar.html', {'ingrediente': ingrediente})


# ===== VISTAS DE VENTAS =====

@login_required
@user_passes_test(es_cliente)
def venta_crear(request):
    """Realizar una venta (clientes autenticados)"""
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            
            # Verificar inventario
            if not venta.producto.hay_inventario_disponible():
                messages.error(request, 'No hay inventario suficiente para este producto.')
                return redirect('producto_lista')
            
            # Calcular total
            venta.total = venta.producto.precio_publico * venta.cantidad
            venta.save()
            
            messages.success(request, f'Venta realizada exitosamente. Total: ${venta.total}')
            return redirect('producto_lista')
    else:
        form = VentaForm()
    
    return render(request, 'heladeria/venta_form.html', {'form': form})


@login_required
@user_passes_test(es_administrador)
def venta_lista(request):
    """Lista de todas las ventas (solo administrador)"""
    ventas = Venta.objects.all().select_related('producto', 'usuario')
    
    # Estadísticas
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
    ventas_hoy = ventas.filter(fecha__date=timezone.now().date())
    total_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0
    
    context = {
        'ventas': ventas[:50],  # Últimas 50 ventas
        'total_ventas': total_ventas,
        'total_hoy': total_hoy,
        'cantidad_hoy': ventas_hoy.count()
    }
    
    return render(request, 'heladeria/venta_lista.html', context)


@login_required
def mis_compras(request):
    """Ver mis compras (usuario autenticado)"""
    ventas = Venta.objects.filter(usuario=request.user).select_related('producto')
    total_gastado = ventas.aggregate(total=Sum('total'))['total'] or 0
    
    context = {
        'ventas': ventas,
        'total_gastado': total_gastado
    }
    
    return render(request, 'heladeria/mis_compras.html', context)


# ===== VISTA DE PRODUCTO MÁS RENTABLE =====

@login_required
@user_passes_test(es_administrador)
def producto_mas_rentable(request):
    """Muestra el producto más rentable (solo administrador)"""
    productos = Producto.objects.all()
    
    if not productos:
        messages.info(request, 'No hay productos registrados.')
        return redirect('dashboard')
    
    # Calcular rentabilidad de cada producto
    productos_rentabilidad = []
    for producto in productos:
        rentabilidad = producto.calcular_rentabilidad()
        productos_rentabilidad.append({
            'producto': producto,
            'rentabilidad': rentabilidad,
            'costo': producto.calcular_costo(),
            'precio': producto.precio_publico
        })
    
    # Ordenar por rentabilidad descendente
    productos_rentabilidad.sort(key=lambda x: x['rentabilidad'], reverse=True)
    
    context = {
        'productos_rentabilidad': productos_rentabilidad,
        'mas_rentable': productos_rentabilidad[0] if productos_rentabilidad else None
    }
    
    return render(request, 'heladeria/producto_rentable.html', context)
