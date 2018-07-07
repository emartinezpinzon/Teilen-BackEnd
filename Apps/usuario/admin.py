from django.contrib import admin
from Apps.usuario.models import Persona, Rol, GithubPersona

admin.site.register(Rol)
admin.site.register(Persona)
admin.site.register(GithubPersona)