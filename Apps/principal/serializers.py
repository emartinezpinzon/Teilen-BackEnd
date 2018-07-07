from rest_framework import serializers

from Apps.usuario.serializers import PersonaSerializer

from Apps.principal.models import  (
    Idea, Proyecto,
    Materia,
    Materia_Persona,
    Proyecto_Alumno,
    Materia_Proyecto,
    Idea_Proyecto,
    Repositorio_Proyecto
)


class IdeaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Idea
        fields = ('id', 'nombre', 'descripcion', 'fecha_creacion', 'persona')


class ProyectoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    docente = PersonaSerializer(read_only=True)

    class Meta:
        model = (Proyecto)
        fields = (
            'id',
            'nombre',
            'descipcion',
            'fecha_creacion',
            'docente'
        )



class MateriaSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Materia
        fields = ('id','nombre','codigo')



class Materia_PersonaSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    materia = MateriaSerializer(read_only=True)
    persona = PersonaSerializer(read_only=True)
    class Meta:
        model = Materia_Persona
        fields = ('id','materia','persona', 'semestre')


class Proyecto_AlumnoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    proyecto = ProyectoSerializer(read_only=True)
    alumno = PersonaSerializer(read_only=True)

    class Meta:
        model = Proyecto_Alumno
        fields = ('id','proyecto','alumno', 'fecha_creacion')

class Materia_ProyectoSerializer(serializers.ModelSerializer):


    materia = MateriaSerializer(read_only=True)
    proyecto = ProyectoSerializer(read_only=True)

    class Meta:
        model = Materia_Proyecto
        fields = ('materia','proyecto')


class Idea_ProyectoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    idea = IdeaSerializer(read_only=True)

    class Meta:
        model = Idea_Proyecto
        fields = ('idea','id')


class Repositorio_ProyectoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Repositorio_Proyecto
        fields = ('id','nombre','link','propietario')

