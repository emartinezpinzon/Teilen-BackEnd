from rest_framework import serializers

from Apps.usuario.models import (
    Rol, Usuario, Persona
)


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = (
            'nombre',
        )


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'documento',
            'first_name',
            'last_name',
            'email',
            'email_institucional',
            'telefono',
            'imagen'
        )


class PersonaSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    persona = UsuarioSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = (
            'codigo',
            'carrera',
            'semestre_actual',
            'año_actual',
            'rol',
            'persona'
        )
