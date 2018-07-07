from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return (self.nombre)


class Usuario(AbstractUser):
    documento = models.CharField(max_length=25)
    imagen = models.TextField()
    email_institucional = models.CharField(max_length=254)
    telefono = models.CharField(max_length=15, null=True)


class Persona(models.Model):
    persona = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    codigo = models.CharField(primary_key=True, max_length=10)
    carrera = models.CharField(max_length=280, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    semestre_actual = models.IntegerField(default=1)
    año_actual = models.DateField(auto_now_add=True)



class GithubPersona(models.Model):
    token = models.TextField()
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
