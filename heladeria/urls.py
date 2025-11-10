from django.urls import path
from . import views

urlpatterns = [
    # Rutas públicas
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Productos (públicos y con permisos)
    path('productos/', views.producto_lista, name='producto_lista'),
    path('productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('productos/rentable/', views.producto_mas_rentable, name='producto_rentable'),
    
    # Ingredientes (solo empleados y admin)
    path('ingredientes/', views.ingrediente_lista, name='ingrediente_lista'),
    path('ingredientes/crear/', views.ingrediente_crear, name='ingrediente_crear'),
    path('ingredientes/<int:pk>/editar/', views.ingrediente_editar, name='ingrediente_editar'),
    path('ingredientes/<int:pk>/eliminar/', views.ingrediente_eliminar, name='ingrediente_eliminar'),
    
    # Ventas
    path('ventas/crear/', views.venta_crear, name='venta_crear'),
    path('ventas/', views.venta_lista, name='venta_lista'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
]
