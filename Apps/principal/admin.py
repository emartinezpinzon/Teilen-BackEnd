from django.contrib import admin
from Apps.principal.models import (
    Materia, Materia_Persona, Materia_Proyecto, Proyecto_Alumno, Proyecto,
    Idea
)

admin.site.register(Materia)
admin.site.register(Materia_Persona)
admin.site.register(Materia_Proyecto)
admin.site.register(Proyecto_Alumno)
admin.site.register(Proyecto)
admin.site.register(Idea)


