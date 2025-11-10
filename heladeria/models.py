from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


# Paso 1: Modelo de Usuario personalizado
# Extendemos el usuario de Django para agregar el campo 'rol'
# Esto permite tener diferentes tipos de usuarios: admin, empleado, cliente

class Usuario(AbstractUser):
    # Definimos los roles disponibles en el sistema
    ROLES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('EMPLEADO', 'Empleado'),
        ('CLIENTE', 'Cliente'),
    ]
    
    # Campo para almacenar el rol del usuario
    # Por defecto, todos los usuarios nuevos serán CLIENTE
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='CLIENTE',
        verbose_name='Rol'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


# Paso 2: Modelo de Ingrediente
# Los ingredientes pueden ser BASES (como helado de vainilla) 
# o COMPLEMENTOS (como chispas de chocolate)

class Ingrediente(models.Model):
    # Tipos de ingredientes
    TIPO_CHOICES = [
        ('BASE', 'Base'),
        ('COMPLEMENTO', 'Complemento'),
    ]
    
    # Campos básicos del ingrediente
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio'
    )
    calorias = models.PositiveIntegerField(verbose_name='Calorías por porción')
    inventario = models.PositiveIntegerField(default=0, verbose_name='Inventario disponible')
    es_vegetariano = models.BooleanField(default=False, verbose_name='Es vegetariano')
    es_sano = models.BooleanField(default=False, verbose_name='Es sano')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name='Tipo')
    
    # Este campo solo se usa si el ingrediente es una BASE
    sabor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Sabor (solo para bases)'
    )
    
    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    # Método para renovar inventario
    # Si es complemento, se pone en 0
    def renovar_inventario(self):
        if self.tipo == 'COMPLEMENTO':
            self.inventario = 0
            self.save()
            return True
        return False


# Paso 3: Modelo de Producto
# Los productos son lo que vendemos: COPAS o MALTEADAS
# Cada producto está compuesto por 3 ingredientes

class Producto(models.Model):
    # Tipos de productos
    TIPO_CHOICES = [
        ('COPA', 'Copa'),
        ('MALTEADA', 'Malteada'),
    ]
    
    # Campos básicos
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    precio_publico = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio al público'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo')
    
    # Campos específicos para COPAS
    tipo_vaso = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Tipo de vaso (solo para copas)'
    )
    
    # Campos específicos para MALTEADAS
    volumen_onzas = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Volumen en onzas (solo para malteadas)'
    )
    
    # Relación con ingredientes (many-to-many)
    # Un producto puede tener varios ingredientes
    # Un ingrediente puede estar en varios productos
    ingredientes = models.ManyToManyField(
        Ingrediente,
        through='ProductoIngrediente',
        related_name='productos',
        verbose_name='Ingredientes'
    )
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    # Método para calcular cuánto nos cuesta hacer el producto
    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes.all())
    
    # Método para calcular calorías totales del producto
    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.ingredientes.all())
    
    # Método para calcular cuánto ganamos vendiendo el producto
    # Rentabilidad = Precio de venta - Costo de producción
    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
    
    # Método para verificar si hay inventario de todos los ingredientes
    def hay_inventario_disponible(self):
        for ingrediente in self.ingredientes.all():
            if ingrediente.inventario <= 0:
                return False
        return True


# Paso 4: Tabla intermedia Producto-Ingrediente
# Esta tabla conecta productos con ingredientes
# Django la usa internamente para la relación many-to-many

class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    ingrediente = models.ForeignKey(
        Ingrediente,
        on_delete=models.CASCADE,
        verbose_name='Ingrediente'
    )
    
    class Meta:
        verbose_name = 'Producto-Ingrediente'
        verbose_name_plural = 'Productos-Ingredientes'
        unique_together = ['producto', 'ingrediente']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.ingrediente.nombre}"


# Paso 5: Modelo de Venta
# Registra cada venta que se hace en la heladería
# Guarda: qué se vendió, quién compró, cuánto pagó y cuándo

class Venta(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='ventas',
        verbose_name='Producto'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ventas',
        verbose_name='Usuario'
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']  # Ordena por fecha descendente (más recientes primero)
    
    def __str__(self):
        return f"Venta #{self.id} - {self.producto.nombre} - ${self.total}"
    
    # Método que se ejecuta automáticamente al guardar una venta
    # Descuenta el inventario de los ingredientes
    def save(self, *args, **kwargs):
        # Solo descuenta inventario cuando se crea la venta (no al actualizarla)
        if not self.pk:
            for ingrediente in self.producto.ingredientes.all():
                if ingrediente.inventario > 0:
                    ingrediente.inventario -= self.cantidad
                    ingrediente.save()
        
        super().save(*args, **kwargs)
