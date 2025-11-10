"""
Script para poblar la base de datos con datos de prueba
Ejecutar con: python manage.py shell < poblar_datos.py
"""

from heladeria.models import Usuario, Ingrediente, Producto, ProductoIngrediente, Venta
from django.contrib.auth.hashers import make_password

print("🍦 Iniciando población de datos...\n")

# Crear usuarios de prueba
print("👥 Creando usuarios...")
empleado, created = Usuario.objects.get_or_create(
    username='empleado1',
    defaults={
        'email': 'empleado@heladeria.com',
        'password': make_password('1234'),
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'rol': 'EMPLEADO'
    }
)
if created:
    print(f"   ✓ Usuario empleado creado: {empleado.username}")
else:
    print(f"   - Usuario empleado ya existe: {empleado.username}")

cliente, created = Usuario.objects.get_or_create(
    username='cliente1',
    defaults={
        'email': 'cliente@heladeria.com',
        'password': make_password('1234'),
        'first_name': 'María',
        'last_name': 'García',
        'rol': 'CLIENTE'
    }
)
if created:
    print(f"   ✓ Usuario cliente creado: {cliente.username}")
else:
    print(f"   - Usuario cliente ya existe: {cliente.username}")

# Crear ingredientes BASE
print("\n🧊 Creando ingredientes BASE...")
bases = [
    {'nombre': 'Helado de Vainilla', 'precio': 2.50, 'calorias': 150, 'inventario': 50, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'BASE', 'sabor': 'Vainilla'},
    {'nombre': 'Helado de Chocolate', 'precio': 2.80, 'calorias': 180, 'inventario': 45, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'BASE', 'sabor': 'Chocolate'},
    {'nombre': 'Helado de Fresa', 'precio': 2.70, 'calorias': 140, 'inventario': 40, 
     'es_vegetariano': True, 'es_sano': True, 'tipo': 'BASE', 'sabor': 'Fresa'},
    {'nombre': 'Helado de Mango', 'precio': 3.00, 'calorias': 130, 'inventario': 35, 
     'es_vegetariano': True, 'es_sano': True, 'tipo': 'BASE', 'sabor': 'Mango'},
]

for base in bases:
    obj, created = Ingrediente.objects.get_or_create(
        nombre=base['nombre'],
        defaults=base
    )
    if created:
        print(f"   ✓ Base creada: {obj.nombre}")
    else:
        print(f"   - Base ya existe: {obj.nombre}")

# Crear ingredientes COMPLEMENTO
print("\n🍫 Creando ingredientes COMPLEMENTO...")
complementos = [
    {'nombre': 'Chispas de Chocolate', 'precio': 0.50, 'calorias': 50, 'inventario': 100, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'COMPLEMENTO'},
    {'nombre': 'Nueces', 'precio': 0.80, 'calorias': 80, 'inventario': 80, 
     'es_vegetariano': True, 'es_sano': True, 'tipo': 'COMPLEMENTO'},
    {'nombre': 'Crema Batida', 'precio': 0.60, 'calorias': 70, 'inventario': 90, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'COMPLEMENTO'},
    {'nombre': 'Salsa de Caramelo', 'precio': 0.70, 'calorias': 60, 'inventario': 85, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'COMPLEMENTO'},
    {'nombre': 'Frutas Frescas', 'precio': 1.00, 'calorias': 40, 'inventario': 70, 
     'es_vegetariano': True, 'es_sano': True, 'tipo': 'COMPLEMENTO'},
    {'nombre': 'Galleta Oreo', 'precio': 0.90, 'calorias': 100, 'inventario': 75, 
     'es_vegetariano': True, 'es_sano': False, 'tipo': 'COMPLEMENTO'},
]

for comp in complementos:
    obj, created = Ingrediente.objects.get_or_create(
        nombre=comp['nombre'],
        defaults=comp
    )
    if created:
        print(f"   ✓ Complemento creado: {obj.nombre}")
    else:
        print(f"   - Complemento ya existe: {obj.nombre}")

# Crear productos
print("\n🍨 Creando productos...")

# Copa 1: Delicia de Vainilla
copa1, created = Producto.objects.get_or_create(
    nombre='Delicia de Vainilla',
    defaults={
        'precio_publico': 5.50,
        'tipo': 'COPA',
        'tipo_vaso': 'Copa Grande'
    }
)
if created:
    print(f"   ✓ Producto creado: {copa1.nombre}")
    # Agregar ingredientes
    ing1 = Ingrediente.objects.get(nombre='Helado de Vainilla')
    ing2 = Ingrediente.objects.get(nombre='Chispas de Chocolate')
    ing3 = Ingrediente.objects.get(nombre='Crema Batida')
    copa1.ingredientes.add(ing1, ing2, ing3)
else:
    print(f"   - Producto ya existe: {copa1.nombre}")

# Copa 2: Chocolate Supremo
copa2, created = Producto.objects.get_or_create(
    nombre='Chocolate Supremo',
    defaults={
        'precio_publico': 6.00,
        'tipo': 'COPA',
        'tipo_vaso': 'Copa Premium'
    }
)
if created:
    print(f"   ✓ Producto creado: {copa2.nombre}")
    ing1 = Ingrediente.objects.get(nombre='Helado de Chocolate')
    ing2 = Ingrediente.objects.get(nombre='Nueces')
    ing3 = Ingrediente.objects.get(nombre='Salsa de Caramelo')
    copa2.ingredientes.add(ing1, ing2, ing3)
else:
    print(f"   - Producto ya existe: {copa2.nombre}")

# Malteada 1: Fresa Natural
malteada1, created = Producto.objects.get_or_create(
    nombre='Fresa Natural',
    defaults={
        'precio_publico': 5.00,
        'tipo': 'MALTEADA',
        'volumen_onzas': 16
    }
)
if created:
    print(f"   ✓ Producto creado: {malteada1.nombre}")
    ing1 = Ingrediente.objects.get(nombre='Helado de Fresa')
    ing2 = Ingrediente.objects.get(nombre='Frutas Frescas')
    ing3 = Ingrediente.objects.get(nombre='Crema Batida')
    malteada1.ingredientes.add(ing1, ing2, ing3)
else:
    print(f"   - Producto ya existe: {malteada1.nombre}")

# Malteada 2: Mango Tropical
malteada2, created = Producto.objects.get_or_create(
    nombre='Mango Tropical',
    defaults={
        'precio_publico': 5.50,
        'tipo': 'MALTEADA',
        'volumen_onzas': 20
    }
)
if created:
    print(f"   ✓ Producto creado: {malteada2.nombre}")
    ing1 = Ingrediente.objects.get(nombre='Helado de Mango')
    ing2 = Ingrediente.objects.get(nombre='Frutas Frescas')
    ing3 = Ingrediente.objects.get(nombre='Crema Batida')
    malteada2.ingredientes.add(ing1, ing2, ing3)
else:
    print(f"   - Producto ya existe: {malteada2.nombre}")

# Copa 3: Oreo Dream
copa3, created = Producto.objects.get_or_create(
    nombre='Oreo Dream',
    defaults={
        'precio_publico': 6.50,
        'tipo': 'COPA',
        'tipo_vaso': 'Copa Premium'
    }
)
if created:
    print(f"   ✓ Producto creado: {copa3.nombre}")
    ing1 = Ingrediente.objects.get(nombre='Helado de Vainilla')
    ing2 = Ingrediente.objects.get(nombre='Galleta Oreo')
    ing3 = Ingrediente.objects.get(nombre='Crema Batida')
    copa3.ingredientes.add(ing1, ing2, ing3)
else:
    print(f"   - Producto ya existe: {copa3.nombre}")

# Crear algunas ventas de ejemplo
print("\n💰 Creando ventas de prueba...")
admin = Usuario.objects.get(username='admin')

venta1, created = Venta.objects.get_or_create(
    producto=copa1,
    usuario=cliente,
    defaults={
        'cantidad': 2,
        'total': copa1.precio_publico * 2
    }
)
if created:
    print(f"   ✓ Venta creada: {venta1}")

venta2, created = Venta.objects.get_or_create(
    producto=malteada1,
    usuario=cliente,
    defaults={
        'cantidad': 1,
        'total': malteada1.precio_publico
    }
)
if created:
    print(f"   ✓ Venta creada: {venta2}")

print("\n✅ ¡Datos poblados exitosamente!")
print("\n📊 Resumen:")
print(f"   - Usuarios: {Usuario.objects.count()}")
print(f"   - Ingredientes: {Ingrediente.objects.count()}")
print(f"   - Productos: {Producto.objects.count()}")
print(f"   - Ventas: {Venta.objects.count()}")
