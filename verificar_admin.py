from heladeria.models import Usuario

# Obtener usuario admin
try:
    admin = Usuario.objects.get(username='admin')
    print(f"✅ Usuario encontrado: {admin.username}")
    print(f"📧 Email: {admin.email}")
    print(f"👤 Rol: {admin.rol}")
    print(f"🔓 Activo: {admin.is_active}")
    print(f"⭐ Superuser: {admin.is_superuser}")
    
    # Resetear contraseña a 1234
    admin.set_password('1234')
    admin.rol = 'ADMINISTRADOR'
    admin.is_active = True
    admin.save()
    
    print("\n✅ Contraseña reseteada a: 1234")
    print("✅ Rol actualizado a: ADMINISTRADOR")
    print("✅ Usuario activado")
    
    # Verificar que la contraseña funciona
    if admin.check_password('1234'):
        print("\n✅✅✅ CONTRASEÑA VERIFICADA CORRECTAMENTE ✅✅✅")
    else:
        print("\n❌ ERROR: La contraseña no coincide")
        
except Usuario.DoesNotExist:
    print("❌ Usuario admin no existe. Creando uno nuevo...")
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@heladeria.com',
        password='1234',
        rol='ADMINISTRADOR'
    )
    print("✅ Usuario admin creado exitosamente")
    print("   Username: admin")
    print("   Password: 1234")
    print("   Rol: ADMINISTRADOR")
