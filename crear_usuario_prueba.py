from heladeria.models import Usuario

# Crear un usuario de prueba completamente nuevo
try:
    # Eliminar si ya existe
    Usuario.objects.filter(username='prueba').delete()
except:
    pass

# Crear usuario nuevo
user = Usuario.objects.create_user(
    username='prueba',
    email='prueba@test.com',
    password='prueba123',
    rol='ADMINISTRADOR'
)

print("✅ Usuario de prueba creado:")
print(f"   Username: prueba")
print(f"   Password: prueba123")
print(f"   Rol: {user.rol}")
print(f"   Activo: {user.is_active}")

# Verificar que la contraseña funciona
if user.check_password('prueba123'):
    print("\n✅ Contraseña verificada correctamente")
else:
    print("\n❌ Error en la contraseña")
