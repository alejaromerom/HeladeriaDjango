# 🚀 Guía de Despliegue - Heladería Delicias

Esta guía te ayudará a desplegar tu aplicación Django en diferentes plataformas para que sea accesible públicamente.

---

## 📋 Tabla de Contenidos

1. [Render.com (Recomendado - Gratis)](#1%EF%B8%8F⃣-rendercom-recomendado---gratis)
2. [Railway (Alternativa)](#2%EF%B8%8F⃣-railway-alternativa)
3. [PythonAnywhere (Opción Simple)](#3%EF%B8%8F⃣-pythonanywhere-opción-simple)
4. [Heroku (Pago)](#4%EF%B8%8F⃣-heroku-pago)
5. [Preparación General](#-preparación-general)

---

## 1️⃣ Render.com (Recomendado - Gratis)

### ✅ Ventajas
- Plan gratuito permanente
- Despliegue automático desde GitHub
- PostgreSQL incluido gratis
- HTTPS automático
- Fácil de usar

### 📝 Pasos

#### Paso 1: Preparar archivos necesarios

**1.1 Crear `render.yaml`** (en la raíz del proyecto)

```yaml
# render.yaml
databases:
  - name: heladeria-db
    databaseName: heladeria_db
    user: heladeria
    plan: free

services:
  - type: web
    name: heladeria-delicias
    env: python
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: heladeria-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
```

**1.2 Crear `build.sh`** (script de build)

```bash
#!/usr/bin/env bash
# build.sh

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

**1.3 Actualizar `requirements.txt`**

Agregar gunicorn y configurar para producción:

```txt
Django==4.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.1.0
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
```

**1.4 Actualizar `settings.py`**

Agregar al final:

```python
# settings.py

import dj_database_url

# ... código existente ...

# Configuración para producción
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Database from DATABASE_URL
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
    
    # WhiteNoise configuration
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Allowed hosts desde variable de entorno
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

#### Paso 2: Subir a GitHub

```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

#### Paso 3: Desplegar en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en "New +" → "Blueprint"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el `render.yaml`
5. Click en "Apply"
6. Espera 5-10 minutos mientras despliega

#### Paso 4: Crear superusuario

Una vez desplegado, ve a la consola (Shell) en Render:

```bash
python manage.py createsuperuser
```

**¡Listo!** Tu app estará en: `https://heladeria-delicias.onrender.com`

---

## 2️⃣ Railway (Alternativa)

### ✅ Ventajas
- $5 USD gratis mensuales
- Muy rápido
- PostgreSQL incluido
- CLI potente

### 📝 Pasos

#### Paso 1: Instalar Railway CLI

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex
```

#### Paso 2: Login y deploy

```bash
# Login
railway login

# Inicializar proyecto
railway init

# Agregar PostgreSQL
railway add -d postgres

# Desplegar
railway up

# Ver variables de entorno
railway variables

# Abrir en navegador
railway open
```

#### Paso 3: Configurar variables

En el dashboard de Railway, agrega:

```
SECRET_KEY=tu-secret-key-segura
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=(automático)
```

**URL:** `https://tu-app.railway.app`

---

## 3️⃣ PythonAnywhere (Opción Simple)

### ✅ Ventajas
- Plan gratuito básico
- No requiere Docker
- Ideal para principiantes
- Interface web amigable

### ⚠️ Desventajas
- Límites en plan gratuito
- PostgreSQL solo en plan pago
- URL: `usuario.pythonanywhere.com`

### 📝 Pasos

1. Regístrate en [pythonanywhere.com](https://www.pythonanywhere.com)
2. Ve a "Web" → "Add a new web app"
3. Selecciona Django y Python 3.11
4. Sube tu código via Git o archivos
5. Configura virtualenv y requirements
6. Configura WSGI file
7. Reload la web app

**Nota:** En el plan gratuito usarás SQLite en vez de PostgreSQL.

---

## 4️⃣ Heroku (Pago)

### ⚠️ Ya no tiene plan gratuito

Desde Nov 2022, Heroku eliminó su plan gratuito.

**Costo:** Desde $7/mes

Si decides usarlo:

1. Crear `Procfile`:
```
web: gunicorn config.wsgi
```

2. Crear `runtime.txt`:
```
python-3.11.0
```

3. Desplegar:
```bash
heroku login
heroku create heladeria-delicias
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 🛠️ Preparación General

### Archivos necesarios para cualquier plataforma:

#### 1. `requirements.txt` actualizado

```txt
Django==4.2.7
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.1.0
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
```

#### 2. Modificar `settings.py`

```python
import os
from decouple import config
import dj_database_url

# SECRET_KEY desde variable de entorno
SECRET_KEY = config('SECRET_KEY', default='dev-secret-key-change-in-production')

# DEBUG desde variable de entorno
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS desde variable de entorno
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise para servir archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Agregar aquí
    # ... resto del middleware
]

# Configuración de producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

#### 3. Crear `.gitignore`

```gitignore
# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 📊 Comparación de Plataformas

| Característica | Render | Railway | PythonAnywhere | Heroku |
|---------------|--------|---------|----------------|--------|
| **Precio** | Gratis | $5/mes gratis | Gratis (limitado) | Desde $7/mes |
| **PostgreSQL** | ✅ Gratis | ✅ Incluido | ❌ Solo pago | ✅ Incluido |
| **Auto Deploy** | ✅ | ✅ | ❌ | ✅ |
| **HTTPS** | ✅ Automático | ✅ Automático | ✅ | ✅ |
| **Dominio** | .onrender.com | .railway.app | .pythonanywhere.com | .herokuapp.com |
| **Dificultad** | Fácil | Media | Fácil | Media |
| **Recomendado para** | Proyectos escolares | Proyectos serios | Pruebas rápidas | Producción |

---

## 🎯 Mi Recomendación

### Para tu proyecto escolar: **Render.com**

**Por qué:**
1. ✅ **100% gratis** - No requiere tarjeta de crédito
2. ✅ **PostgreSQL incluido** - Tu app usa PostgreSQL
3. ✅ **Fácil configuración** - Solo subir a GitHub
4. ✅ **URL profesional** - `heladeria-delicias.onrender.com`
5. ✅ **Auto deploy** - Cada push a GitHub actualiza la app
6. ✅ **HTTPS automático** - Seguro por defecto

**Desventaja:**
- La app "duerme" después de 15 min de inactividad (tarda ~1 min en despertar)

---

## 🚀 Pasos Rápidos para Render (Resumen)

1. **Instalar dependencias nuevas:**
```bash
pip install gunicorn whitenoise dj-database-url
pip freeze > requirements.txt
```

2. **Crear archivos:**
   - `render.yaml` (configuración)
   - `build.sh` (script de build)
   - Actualizar `settings.py`

3. **Subir a GitHub:**
```bash
git add .
git commit -m "Preparar despliegue"
git push
```

4. **Desplegar en Render:**
   - Ir a render.com
   - New Blueprint
   - Conectar repo
   - Apply

5. **Crear superusuario:**
```bash
# En la consola de Render
python manage.py createsuperuser
```

**¡Listo en 10 minutos!** 🎉

---

## 📞 Troubleshooting

### Error: "Application failed to start"
- Verifica que `gunicorn` esté en `requirements.txt`
- Revisa los logs en el dashboard de la plataforma
- Verifica que `build.sh` tenga permisos de ejecución

### Error: "Database connection failed"
- Verifica que la variable `DATABASE_URL` esté configurada
- En Render, asegúrate de que el servicio web esté conectado a la BD

### Error: "Static files not loading"
- Ejecuta `python manage.py collectstatic`
- Verifica que `whitenoise` esté instalado
- Revisa la configuración de `STATIC_ROOT`

### La app está muy lenta
- Normal en plan gratuito de Render (cold start)
- Considera usar Railway si necesitas más velocidad

---

## 📚 Recursos Adicionales

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Docs](http://whitenoise.evans.io/)

---

## ✅ Checklist Final

Antes de desplegar, verifica:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` desde variable de entorno
- [ ] `ALLOWED_HOSTS` configurado
- [ ] `gunicorn` en requirements.txt
- [ ] `whitenoise` configurado
- [ ] `.gitignore` incluye `.env`
- [ ] Migraciones aplicadas
- [ ] Archivos estáticos recolectados
- [ ] Superusuario creado

---

<div align="center">

**🚀 ¡Buena suerte con el despliegue!**

Si tienes problemas, revisa los logs de la plataforma o contacta soporte.

</div>
