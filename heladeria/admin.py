from django.contrib import admin
from .models import Usuario, Ingrediente, Producto, ProductoIngrediente, Venta


# Configuración del panel de administración para Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'rol', 'first_name', 'last_name', 'is_active']
    list_filter = ['rol', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    # Campos que se mostrarán al crear/editar usuario
    fieldsets = (
        ('Información básica', {
            'fields': ('username', 'password', 'email')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name')
        }),
        ('Rol y permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )


# Configuración del panel de administración para Ingrediente
@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio', 'calorias', 'inventario', 'es_vegetariano', 'es_sano']
    list_filter = ['tipo', 'es_vegetariano', 'es_sano']
    search_fields = ['nombre', 'sabor']
    ordering = ['nombre']
    
    # Organizar campos por secciones
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'tipo', 'sabor')
        }),
        ('Precio y características', {
            'fields': ('precio', 'calorias', 'inventario')
        }),
        ('Propiedades', {
            'fields': ('es_vegetariano', 'es_sano')
        }),
    )
    
    # Acciones personalizadas
    actions = ['renovar_inventario_complementos']
    
    def renovar_inventario_complementos(self, request, queryset):
        """Acción para renovar inventario de complementos seleccionados"""
        count = 0
        for ingrediente in queryset:
            if ingrediente.renovar_inventario():
                count += 1
        self.message_user(request, f'{count} complementos renovados (inventario en 0).')
    renovar_inventario_complementos.short_description = 'Renovar inventario de complementos'


# Configuración inline para mostrar ingredientes dentro de un producto
class ProductoIngredienteInline(admin.TabularInline):
    model = ProductoIngrediente
    extra = 3  # Muestra 3 campos vacíos para agregar ingredientes
    max_num = 3  # Máximo 3 ingredientes por producto


# Configuración del panel de administración para Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio_publico', 'mostrar_costo', 'mostrar_rentabilidad', 'mostrar_calorias']
    list_filter = ['tipo']
    search_fields = ['nombre']
    ordering = ['nombre']
    inlines = [ProductoIngredienteInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'tipo', 'precio_publico')
        }),
        ('Detalles específicos', {
            'fields': ('tipo_vaso', 'volumen_onzas'),
            'description': 'tipo_vaso solo para COPAS, volumen_onzas solo para MALTEADAS'
        }),
    )
    
    # Métodos para mostrar información calculada
    def mostrar_costo(self, obj):
        """Muestra el costo de producción"""
        return f"${obj.calcular_costo():.2f}"
    mostrar_costo.short_description = 'Costo'
    
    def mostrar_rentabilidad(self, obj):
        """Muestra la rentabilidad del producto"""
        return f"${obj.calcular_rentabilidad():.2f}"
    mostrar_rentabilidad.short_description = 'Rentabilidad'
    
    def mostrar_calorias(self, obj):
        """Muestra las calorías totales"""
        return f"{obj.calcular_calorias()} cal"
    mostrar_calorias.short_description = 'Calorías'


# Configuración del panel de administración para Venta
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'usuario', 'cantidad', 'total', 'fecha']
    list_filter = ['fecha', 'producto']
    search_fields = ['producto__nombre', 'usuario__username']
    ordering = ['-fecha']  # Más recientes primero
    date_hierarchy = 'fecha'  # Navegación por fechas
    
    # Solo lectura (no se pueden editar ventas una vez creadas)
    readonly_fields = ['producto', 'usuario', 'cantidad', 'total', 'fecha']
    
    def has_add_permission(self, request):
        """No permitir agregar ventas desde el admin (se hacen desde la app)"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """No permitir editar ventas"""
        return False
