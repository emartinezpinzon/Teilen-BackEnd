from django.urls import path

from Apps.principal import views

urlpatterns = [
    path('ideas/<int:pk>/me/', views.IdeasList.as_view()),
    path('ideas/', views.IdeaList.as_view()),
    path('ideas/all/', views.AllIdeasList.as_view()),
    path('ideas/<int:pk>/', views.IdeaDetail.as_view()),
    path('proyecto/', views.ProyectoList.as_view()),
    path('proyecto/<int:pk>/', views.ProyectoDeatil.as_view()),
    path('proyecto/<int:proyecto_id>/idea/', views.IdeaProyectoList.as_view()),
    path('proyecto/<int:proyecto_id>/materia/', views.MateriaProyectoList.as_view()),
    path('proyecto/<int:proyecto_id>/estudiante/', views.EstudianteProyectoList.as_view()),
    path('proyecto/<int:proyecto_id>/repositorios/', views.RepostiroioProyectoList.as_view()),
    path('estudiante/materia/<slug:codigo_materia>/', views.EstudianteMateriaList.as_view()),

]
