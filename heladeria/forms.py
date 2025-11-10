from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Ingrediente, Producto, Venta


# Formulario para registro de nuevos usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(max_length=30, required=False, label='Nombre')
    last_name = forms.CharField(max_length=30, required=False, label='Apellido')
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.rol = 'CLIENTE'  # Por defecto todos son clientes
        if commit:
            user.save()
        return user


# Formulario para crear/editar ingredientes
class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'tipo', 'precio', 'calorias', 'inventario', 
                  'es_vegetariano', 'es_sano', 'sabor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-control'}),
            'inventario': forms.NumberInput(attrs={'class': 'form-control'}),
            'es_vegetariano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_sano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sabor': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulario para crear/editar productos
class ProductoForm(forms.ModelForm):
    # Campo para seleccionar los ingredientes (máximo 3)
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Ingredientes (selecciona exactamente 3)'
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'tipo', 'precio_publico', 'tipo_vaso', 'volumen_onzas', 'ingredientes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'precio_publico': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_vaso': forms.TextInput(attrs={'class': 'form-control'}),
            'volumen_onzas': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_ingredientes(self):
        """Validar que se seleccionen exactamente 3 ingredientes"""
        ingredientes = self.cleaned_data.get('ingredientes')
        if ingredientes and ingredientes.count() != 3:
            raise forms.ValidationError('Debes seleccionar exactamente 3 ingredientes.')
        return ingredientes


# Formulario para realizar una venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }
