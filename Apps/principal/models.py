from django.db import models
from Apps.usuario.models import Persona


class Materia(models.Model):
    codigo = models.CharField(max_length=255, primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return (self.nombre)


class Materia_Persona(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)
    semestre = models.IntegerField(default=1)


class Proyecto(models.Model):
    nombre = models.CharField(max_length=180)
    descipcion = models.TextField(null=True)
    repositorio = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)

    docente = models.ForeignKey(Persona, on_delete=models.PROTECT)

    def __str__(self):
        return (self.nombre)


class Proyecto_Alumno(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    alumno = models.ForeignKey(Persona, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)


class Materia_Proyecto(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return (self.nombre)


class Etiqueta_Proyecto(models.Model):
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.PROTECT)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)


class Idea(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)


class Idea_Proyecto(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.PROTECT)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)


class Repositorio_Proyecto(models.Model):
    nombre = models.TextField(null=True)
    link = models.TextField(null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    repositorio_id = models.IntegerField(null=True)
    contribuyentes_url = models.TextField(null=True)
    propietario = models.TextField(null=True)
