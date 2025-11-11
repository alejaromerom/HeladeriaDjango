# 🚀 PASOS RÁPIDOS PARA DESPLEGAR

## ✅ Archivos ya creados:
- ✅ `render.yaml` - Configuración de Render
- ✅ `build.sh` - Script de construcción
- ✅ `requirements.txt` - Actualizado con gunicorn, whitenoise, dj-database-url
- ✅ `settings.py` - Configurado para producción
- ✅ `.gitignore` - Archivos ignorados
- ✅ `GUIA_DESPLIEGUE.md` - Guía completa

## 🎯 OPCIÓN 1: Render.com (GRATIS - RECOMENDADO)

### Paso 1: Subir a GitHub
```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

### Paso 2: Desplegar en Render
1. Ve a https://render.com
2. Crea una cuenta (gratis)
3. Click en "New +" → "Blueprint"
4. Conecta tu repositorio de GitHub: `alejaromerom/HeladeriaDjango`
5. Render detectará automáticamente el `render.yaml`
6. Click en "Apply"
7. Espera 5-10 minutos

### Paso 3: Crear superusuario
Una vez desplegado, ve al dashboard de Render:
1. Click en tu servicio "heladeria-delicias"
2. Click en "Shell" (terminal)
3. Ejecuta:
```bash
python manage.py createsuperuser
```

### Paso 4: ¡Listo!
Tu app estará disponible en:
```
https://heladeria-delicias.onrender.com
```

---

## 🎯 OPCIÓN 2: Railway (Alternativa - $5 gratis/mes)

### Paso 1: Instalar Railway CLI
```bash
# Windows PowerShell
iwr https://railway.app/install.ps1 | iex
```

### Paso 2: Desplegar
```bash
railway login
railway init
railway add -d postgres
railway up
```

### Paso 3: Crear superusuario
```bash
railway run python manage.py createsuperuser
```

### Paso 4: Abrir app
```bash
railway open
```

---

## ⚠️ IMPORTANTE - Antes de desplegar

### Instalar nuevas dependencias (opcional, solo para probar local):
```bash
pip install gunicorn whitenoise dj-database-url
```

### Variables de entorno que Render configurará automáticamente:
- `DATABASE_URL` - Conexión a PostgreSQL
- `SECRET_KEY` - Clave secreta de Django
- `DEBUG` - False en producción
- `ALLOWED_HOSTS` - .onrender.com

---

## 📊 Comparación

| Plataforma | Precio | PostgreSQL | Tiempo Setup | URL |
|------------|--------|------------|--------------|-----|
| **Render** | Gratis | ✅ Incluido | 10 min | .onrender.com |
| **Railway** | $5/mes | ✅ Incluido | 5 min | .railway.app |

---

## 🐛 Troubleshooting

### "Application failed to start"
- Revisa los logs en el dashboard
- Verifica que `build.sh` se ejecutó correctamente

### "Database connection failed"
- Espera a que la BD termine de inicializarse
- Verifica que el servicio web esté conectado a la BD en el dashboard

### "Static files not found"
- Normal en desarrollo local
- En Render se recolectan automáticamente con `collectstatic`

---

## 📞 Ayuda

Si tienes problemas:
1. Lee la guía completa: `GUIA_DESPLIEGUE.md`
2. Revisa los logs en el dashboard de Render
3. Consulta: https://render.com/docs

---

## ✨ Después del despliegue

1. **Prueba la app**: Abre la URL
2. **Crea superusuario**: Para acceder al admin
3. **Crea usuarios de prueba**: admin, empleado1, cliente1
4. **Pobla con datos**: Crea ingredientes y productos
5. **Comparte la URL**: En tu README y exposición

---

<div align="center">

**🎉 ¡Tu app estará en internet en menos de 15 minutos!**

URL final: `https://heladeria-delicias.onrender.com`

</div>
