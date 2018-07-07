from django.conf.urls import url

from Apps.usuario import views
from django.urls import path

urlpatterns = [
    path('supersesion/', views.SesionDocente.as_view()),
    path('sesion/', views.SesionEstudiante.as_view()),
    path('estudiante/', views.EstudianteList.as_view()),
    path('info/', views.PersonaDetail.as_view()),
    path('materia/', views.MateriaList.as_view()),
    path('proyecto/', views.ProyectList.as_view()),

    path('proyecto/docente/', views.ProyectoDocenteList.as_view()),
    path('github/', views.GithubMiddleware.as_view()),
    path('github/repos/', views.RepositoriosGithubList.as_view())

]
