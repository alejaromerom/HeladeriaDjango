# COMANDO PARA CREAR EMPLEADO MANUALMENTE
# Ejecuta: Get-Content crear_empleado_manual.py | docker-compose exec -T web python manage.py shell

from heladeria.models import Usuario

# Crear empleado
empleado = Usuario.objects.create_user(
    username='empleado2',
    email='empleado2@heladeria.com',
    password='empleado123',
    rol='EMPLEADO'  # ⭐ Esta es la línea clave que define el rol
)

print(f"✅ Empleado creado: {empleado.username}")
print(f"   Rol: {empleado.rol}")
print(f"   Password: empleado123")
