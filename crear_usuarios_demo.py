from heladeria.models import Usuario

# Limpiar usuarios anteriores (excepto admin)
Usuario.objects.filter(username__in=['empleado1', 'cliente1']).delete()

# 1. ADMINISTRADOR (ya existe, solo actualizamos)
try:
    admin = Usuario.objects.get(username='admin')
    admin.set_password('admin123')
    admin.rol = 'ADMINISTRADOR'
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    print("✅ ADMINISTRADOR actualizado:")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   Rol: {admin.rol}")
except Usuario.DoesNotExist:
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@heladeria.com',
        password='admin123',
        rol='ADMINISTRADOR'
    )
    print("✅ ADMINISTRADOR creado:")
    print(f"   Username: admin")
    print(f"   Password: admin123")

# 2. EMPLEADO
empleado = Usuario.objects.create_user(
    username='empleado1',
    email='empleado@heladeria.com',
    password='empleado123',
    rol='EMPLEADO'
)
print("\n✅ EMPLEADO creado:")
print(f"   Username: empleado1")
print(f"   Password: empleado123")
print(f"   Rol: {empleado.rol}")

# 3. CLIENTE
cliente = Usuario.objects.create_user(
    username='cliente1',
    email='cliente@heladeria.com',
    password='cliente123',
    rol='CLIENTE'
)
print("\n✅ CLIENTE creado:")
print(f"   Username: cliente1")
print(f"   Password: cliente123")
print(f"   Rol: {cliente.rol}")

print("\n" + "="*50)
print("🎯 RESUMEN DE USUARIOS PARA LA EXPOSICIÓN:")
print("="*50)
print("\n👨‍💼 ADMINISTRADOR (acceso completo):")
print("   Username: admin | Password: admin123")
print("\n👷 EMPLEADO (gestiona productos e ingredientes):")
print("   Username: empleado1 | Password: empleado123")
print("\n🧑 CLIENTE (solo puede comprar y ver sus compras):")
print("   Username: cliente1 | Password: cliente123")
print("="*50)
