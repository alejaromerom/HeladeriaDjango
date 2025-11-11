# 🍦 Heladería Delicias

Una aplicación web completa para la gestión de una heladería, desarrollada con Django y PostgreSQL. Sistema de inventario automático, control de usuarios por roles y cálculo de rentabilidad en tiempo real.

![Django](https://img.shields.io/badge/Django-4.2.7-green?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat&logo=docker)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple?style=flat&logo=bootstrap)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Modelos de Datos](#-modelos-de-datos)
- [Sistema de Permisos](#-sistema-de-permisos)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características

### 🔐 Sistema de Autenticación y Roles
- **3 tipos de usuarios**: Administrador, Empleado y Cliente
- Control de acceso basado en roles (RBAC)
- Registro y login seguros con Django Auth

### 📦 Gestión de Inventario
- **Descuento automático** de inventario al realizar ventas
- Control de ingredientes: bases y complementos
- Alertas de stock bajo

### 💰 Análisis de Rentabilidad
- Cálculo automático de costos de producción
- Análisis de rentabilidad por producto
- Estadísticas de ventas en tiempo real

### 🛒 Sistema de Ventas
- Proceso de venta intuitivo
- Validación de inventario antes de confirmar
- Historial de compras por usuario

### 🎨 Interfaz Moderna
- Diseño responsivo con Bootstrap 5
- Colores pasteles personalizados
- Experiencia de usuario optimizada

---

## 🛠️ Tecnologías

### Backend
- **Django 4.2.7** - Framework web Python
- **PostgreSQL 15** - Base de datos relacional
- **Python 3.11+** - Lenguaje de programación

### Frontend
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **HTML5 & CSS3** - Maquetación

### DevOps
- **Docker & Docker Compose** - Contenedorización
- **Gunicorn** - Servidor WSGI (producción)

### Dependencias Python
```
Django==4.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.1.0
```

---

## 🏗️ Arquitectura

### Patrón MVT (Model-View-Template)

```
┌─────────────────────────────────────────────┐
│              Django Application              │
├─────────────────────────────────────────────┤
│  Models (ORM)                               │
│  ├─ Usuario (extends AbstractUser)         │
│  ├─ Ingrediente                             │
│  ├─ Producto (ManyToMany con Ingrediente)  │
│  ├─ ProductoIngrediente (tabla intermedia) │
│  └─ Venta (con save() override)            │
├─────────────────────────────────────────────┤
│  Views (Lógica de Negocio)                 │
│  ├─ Sistema de permisos (decoradores)      │
│  ├─ CRUD Productos                          │
│  ├─ CRUD Ingredientes                       │
│  └─ Sistema de ventas                       │
├─────────────────────────────────────────────┤
│  Templates (Interfaz)                       │
│  ├─ base.html (template base)              │
│  ├─ 16 templates HTML                       │
│  └─ Bootstrap 5 personalizado              │
└─────────────────────────────────────────────┘
         ↓                    ↑
    PostgreSQL            Browser
```

### Diagrama Entidad-Relación

```
┌─────────────┐
│   USUARIO   │
│─────────────│
│ id (PK)     │
│ username    │
│ password    │
│ rol ⭐      │ (ADMINISTRADOR/EMPLEADO/CLIENTE)
└─────────────┘
       │ 1
       │
       │ N
       ↓
┌─────────────┐       N ┌──────────────┐ 1
│    VENTA    │────────→│   PRODUCTO   │
│─────────────│         │──────────────│
│ id (PK)     │         │ id (PK)      │
│ usuario_id  │         │ nombre       │
│ producto_id │         │ precio       │
│ cantidad    │         │ tipo         │
│ total       │         └──────────────┘
│ fecha       │                ↕
└─────────────┘         MUCHOS A MUCHOS
                               ↕
                   ┌────────────────────┐
                   │ PRODUCTO_          │
                   │ INGREDIENTE        │
                   │────────────────────│
                   │ id (PK)            │
                   │ producto_id (FK)   │
                   │ ingrediente_id (FK)│
                   └────────────────────┘
                               ↕
                        ┌──────────────┐
                        │ INGREDIENTE  │
                        │──────────────│
                        │ id (PK)      │
                        │ nombre       │
                        │ precio       │
                        │ calorias     │
                        │ inventario ⭐ │
                        │ tipo         │
                        └──────────────┘
```

---

## 🚀 Instalación

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/alejaromerom/HeladeriaDjango.git
cd HeladeriaDjango
```

2. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
DB_NAME=heladeria_db
DB_USER=heladeria
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=5432
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
```

3. **Levantar los contenedores**
```bash
docker-compose up -d
```

4. **Aplicar migraciones** (si es necesario)
```bash
docker-compose exec web python manage.py migrate
```

5. **Crear superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Acceder a la aplicación**
```
http://localhost:8000
```

---

## 📖 Uso

### Usuarios de Prueba

La aplicación viene con usuarios de demostración:

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| `admin` | `admin123` | Administrador | Acceso total |
| `empleado1` | `empleado123` | Empleado | CRUD productos e ingredientes |
| `cliente1` | `cliente123` | Cliente | Realizar compras |

### Flujo de Trabajo

#### 👨‍💼 Como Administrador
1. Login con credenciales de admin
2. Acceso al panel de estadísticas
3. Ver todas las ventas y reportes
4. Gestionar usuarios (Django Admin)

#### 👨‍🍳 Como Empleado
1. Login con credenciales de empleado
2. Crear/editar ingredientes
3. Crear/editar productos (seleccionando 3 ingredientes)
4. Ver inventario

#### 🧑‍🦱 Como Cliente
1. Registro o login
2. Ver catálogo de productos
3. Realizar compras
4. Ver historial de compras

---

## 🗄️ Modelos de Datos

### Usuario
Extiende `AbstractUser` de Django con campo personalizado:
- `rol`: ADMINISTRADOR | EMPLEADO | CLIENTE

### Ingrediente
- `nombre`: string único
- `tipo`: BASE | COMPLEMENTO
- `precio`: decimal
- `calorias`: entero positivo
- `inventario`: entero (se descuenta automáticamente)
- `es_vegetariano`: booleano
- `es_sano`: booleano
- `sabor`: string (solo para bases)

**Métodos:**
- `renovar_inventario()`: Reinicia inventario de complementos

### Producto
- `nombre`: string único
- `tipo`: COPA | MALTEADA
- `precio_publico`: decimal
- `tipo_vaso`: string (solo copas)
- `volumen_onzas`: entero (solo malteadas)
- `ingredientes`: ManyToMany con Ingrediente

**Métodos:**
- `calcular_costo()`: Suma precios de ingredientes
- `calcular_calorias()`: Suma calorías de ingredientes
- `calcular_rentabilidad()`: precio_publico - costo
- `hay_inventario_disponible()`: Verifica stock

### Venta
- `producto`: ForeignKey a Producto
- `usuario`: ForeignKey a Usuario
- `cantidad`: entero positivo
- `total`: decimal
- `fecha`: datetime automático

**Método especial:**
- `save()` override: **Descuenta inventario automáticamente** al crear venta

---

## 🔒 Sistema de Permisos

### Funciones Verificadoras (views.py)

```python
# 🔴 Llave Roja - Solo Administradores
@user_passes_test(es_administrador)

# 🟡 Llave Amarilla - Empleados + Admins
@user_passes_test(es_empleado)

# 🟢 Llave Verde - Todos los autenticados
@user_passes_test(es_cliente)
```

### Matriz de Permisos

| Acción | Cliente | Empleado | Admin |
|--------|---------|----------|-------|
| Ver productos | ✅ | ✅ | ✅ |
| Realizar compra | ✅ | ✅ | ✅ |
| Ver mis compras | ✅ | ✅ | ✅ |
| Crear ingrediente | ❌ | ✅ | ✅ |
| Editar ingrediente | ❌ | ✅ | ✅ |
| Eliminar ingrediente | ❌ | ✅ | ✅ |
| Crear producto | ❌ | ✅ | ✅ |
| Editar producto | ❌ | ✅ | ✅ |
| Eliminar producto | ❌ | ✅ | ✅ |
| Ver todas las ventas | ❌ | ❌ | ✅ |
| Ver estadísticas | ❌ | ❌ | ✅ |
| Producto más rentable | ❌ | ❌ | ✅ |

---

## 📸 Capturas de Pantalla

### Página Principal
![Home](docs/screenshots/home.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Gestión de Productos
![Productos](docs/screenshots/productos.png)

### Sistema de Ventas
![Ventas](docs/screenshots/ventas.png)

---

## 📁 Estructura del Proyecto

```
HeladeriaDjango/
├── 📁 config/                    # Configuración Django
│   ├── settings.py              # Configuración principal
│   ├── urls.py                  # URLs del proyecto
│   └── wsgi.py                  # Punto de entrada WSGI
│
├── 📁 heladeria/                 # Aplicación principal
│   ├── 📁 migrations/           # Migraciones de BD
│   ├── 📁 templates/            # Templates HTML
│   │   └── 📁 heladeria/
│   │       ├── base.html        # Template base
│   │       ├── home.html        # Página principal
│   │       ├── dashboard.html   # Panel de control
│   │       └── ... (16 templates)
│   ├── models.py                # 5 modelos (236 líneas)
│   ├── views.py                 # 20+ vistas (332 líneas)
│   ├── forms.py                 # 4 formularios
│   ├── urls.py                  # URLs de la app
│   └── admin.py                 # Configuración admin
│
├── 📁 scripts/                   # Scripts de utilidad
│   ├── verificar_admin.py       # Verificar/crear admin
│   └── crear_usuarios_demo.py   # Crear datos de prueba
│
├── 📄 docker-compose.yml         # Orquestación Docker
├── 📄 Dockerfile                 # Imagen Docker
├── 📄 requirements.txt           # Dependencias Python
├── 📄 .env                       # Variables de entorno
├── 📄 manage.py                  # CLI Django
└── 📄 README.md                  # Este archivo
```

---

## 🎯 Características Técnicas Destacadas

### 1. Descuento Automático de Inventario
```python
# models.py - Modelo Venta
def save(self, *args, **kwargs):
    if not self.pk:  # Solo en ventas nuevas
        for ingrediente in self.producto.ingredientes.all():
            if ingrediente.inventario > 0:
                ingrediente.inventario -= self.cantidad
                ingrediente.save()
    super().save(*args, **kwargs)
```

### 2. Validación de Formularios
```python
# forms.py - ProductoForm
def clean_ingredientes(self):
    ingredientes = self.cleaned_data.get('ingredientes')
    if ingredientes and ingredientes.count() != 3:
        raise forms.ValidationError('Debes seleccionar exactamente 3 ingredientes.')
    return ingredientes
```

### 3. Optimización de Consultas
```python
# views.py - Uso de select_related
ventas = Venta.objects.all().select_related('producto', 'usuario')
# Evita el problema N+1 de consultas
```

### 4. Control de Acceso Robusto
```python
# views.py - Decoradores en cascada
@login_required
@user_passes_test(es_administrador)
def venta_lista(request):
    # Solo administradores autenticados
```

---

## 🧪 Testing

### Ejecutar tests
```bash
docker-compose exec web python manage.py test
```

### Poblar base de datos con datos de prueba
```bash
docker-compose exec web python scripts/crear_usuarios_demo.py
```

---

## 🐳 Docker

### Comandos útiles

```bash
# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down

# Reconstruir imagen
docker-compose up -d --build

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Acceder a PostgreSQL
docker-compose exec db psql -U heladeria -d heladeria_db
```

---

## 🤝 Contribución

Las contribuciones son bienvenidas! Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Documentación Adicional

- [Guía de Exposición Completa](GUIA_EXPOSICION_COMPLETA.md)
- [Guía de Exposición en Slides](GUIA_EXPOSICION_SLIDES.md)
- [Script de Exposición](SCRIPT_EXPOSICION_COMPLETO.md)
- [Explicación del Código Resumida](EXPLICACION_CODIGO_RESUMIDA.md)

---

## 👨‍💻 Autor

**Alejandro Romero**
- GitHub: [@alejaromerom](https://github.com/alejaromerom)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Django Software Foundation por el excelente framework
- Bootstrap team por el framework CSS
- PostgreSQL Global Development Group
- Comunidad de código abierto

---

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la [documentación adicional](#-documentación-adicional)
2. Abre un [issue](https://github.com/alejaromerom/HeladeriaDjango/issues)
3. Contacta al autor

---

<div align="center">

**⭐ Si te gustó este proyecto, dale una estrella!**

Hecho con ❤️ y mucho ☕ por [Alejandra Romero](https://github.com/alejaromerom)

</div>
