from django.shortcuts import render
from django.http import (
        Http404,
        JsonResponse,
        HttpResponse
    )

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from Apps.usuario.models import Persona

from Apps.principal.models import (
        Idea,
        Proyecto,
        Idea_Proyecto,
        Materia_Persona,
        Materia_Proyecto,
        Proyecto_Alumno,
        Repositorio_Proyecto
    )

from Apps.principal.serializers import (
        IdeaSerializer,
        ProyectoSerializer,
        Materia_PersonaSerializer,
        Materia_ProyectoSerializer,
        Proyecto_AlumnoSerializer,
        Idea_ProyectoSerializer,
        Repositorio_ProyectoSerializer
    )


"""IdeaList Es el controlador encargado de los servicios dirigidos a ideas.

Usa jsonparser ya que al utilizar servicios nace la necesidad de envíar
estructuras de datos complejos

JSON es un lenguaje universal por eso la necesidad de
estandirizar la comunicacion.

JsonParse hace  que la informacion que llege por request se ha representada
con diccionarios en python y no en texto simple.

"""


class IdeasList(APIView):
    """Bajo una función get retorna el listado de las ideas de una persona.

    Verifica la recepción de un token de conexión, consulta, serializa
    y retorna un listado de ideas pertenecientes a una persona

    """
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        ideas = Idea.objects.filter(persona_id=pk)
        serializer = IdeaSerializer(ideas, many=True)

        return Response(serializer.data)


class AllIdeasList(APIView):
    """Bajo una función get retorna el listado de todas las ideas registradas.

    Verifica la recepción de un token de conexión, consulta, serializa
    y retorna un listado con las ideas registradas en el sistema

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        ideas = Idea.objects.all()
        serializer = IdeaSerializer(ideas, many=True)

        return Response(serializer.data)


class IdeaList(APIView):
    """Realiza varias acciones sobre el modelo Idea.

    Verifica la recepción de un token de conexión, y dependiendo
    de la función consulta o crea ideas

    Bajo la función get consulta las ideas pertenecientes a otros
    usuarios (verifica el usuario a excluir en la sesión)
    y retorna un listado de ideas pertenecientes a otras personas

    Bajo la función post recibe los datos de la petición y crea
    una nueva idea del usuario que tiene la sesión activa. Retorna
    un estado 201 para confirmar la creación de la idea

    """
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        ideas = Idea.objects.filter(persona_id = request.user.username)
        serializer = IdeaSerializer(ideas, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):

        nombre = request.data['nombre']
        descripcion = request.data['descripcion']

        if len(nombre)==0 or len(descripcion)==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        idea = Idea(nombre=nombre, descripcion=descripcion, persona_id=request.user.username)
        idea.save()

        return Response(status=status.HTTP_201_CREATED)


class IdeaDetail(APIView):
    """Realiza varias acciones sobre el modelo Idea.

    Verifica la recepción de un token de conexión, y dependiendo
    de la función consulta, actualiza o elimina una idea

    Bajo la función get obtiene una idea del usuario y retorna
    la información de la idea

    Bajo la función put recibe los datos de la petición y actualiza
    la idea envíada del usuario que tiene la sesión activa. Retorna
    la información de la idea actualizada o un estado 400 si algo
    sale mal

    Bajo la función delete elimina una idea del usuario y retorna un
    estado 204

    """
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Idea.objects.get(pk=pk)
        except Idea.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Idea = self.get_object(pk)
        serializer = IdeaSerializer(Idea)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        idea = self.get_object(pk)
        serializer = IdeaSerializer(idea, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        restaurante = self.get_object(pk)
        restaurante.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProyectoList(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request,format=None):
        titulo = request.data['titulo']
        idea = request.data['idea']
        estudiantes = request.data['estudiantes']
        materias = request.data['materias']

        mail = {}

        if len(materias)>0:
            proyecto = Proyecto(nombre=titulo,docente_id=request.user.persona.codigo)
            proyecto.save()

            mail["docente"] = request.user.first_name + " " +request.user.last_name
            mail["proyecto"] = titulo

            for m in materias:
                materia_proyecto = Materia_Proyecto(materia_id=m['codigo'], proyecto_id=proyecto.pk )
                materia_proyecto.save()

                mail["materia"] = m

        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if len(estudiantes)>0:
            mail["estudiantes"] = estudiantes

            for e in estudiantes:
                p = Proyecto_Alumno(proyecto_id=proyecto.pk, alumno_id=e['codigo'])
                p.save()

        if idea:
            proyectoidea = Idea_Proyecto(proyecto_id=proyecto.pk,idea_id=idea['id'])
            proyectoidea.save()


        print("============================== D A T O S === C O R R E O ==============================")
        print(mail)
        print("============================== F I N ==============================")

        """ self.correo() """

        return Response(status=status.HTTP_201_CREATED)


    def get(self,request,format=None):
        """Lista todos los proyectos registrados.

        Obtiene una lista de proyectos, la serializa y genera una respuesta
        con ella

        """
        proyectos = Proyecto.objects.all()
        serializer = ProyectoSerializer(proyectos, many=True)

        return Response(serializer.data)

class ProyectoDeatil(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self,pk):
        try:
            return Proyecto.objects.get(pk=pk)
        except:
            raise Http404


    def get(self,request,pk,format=None):
        proyecto = self.get_object(pk)
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data)

    def put(self,request,pk,forma=None):
        proyecto = self.get_object(pk)
        titulo = request.data['nombre']
        try:
            idea = request.data['idea']
        except:
            idea = None

        estudiantes = request.data['estudiantes']
        materias = request.data['materias']
        repositorios = request.data['repos']


        if len(materias)>0:
            for m in materias:
                try:
                    materia = Materia_Proyecto.objects.get(materia_id=m['materia']['codigo'], proyecto_id=pk)

                except:

                    materia = Materia_Proyecto(materia_id=m['materia']['codigo'], proyecto_id=pk)
                    materia.save()



        if len(estudiantes)>0:
            for e in estudiantes:
                try:
                    estudiante = Proyecto_Alumno.objects.get(alumno_id=e['alumno']['codigo'], proyecto_id=pk)
                except:
                    estudiante = Proyecto_Alumno(e['codigo'], proyecto_id=pk)
                    estudiante.save()





        if len(repositorios)>0:
            for repo in repositorios:
                try:
                    repositorio = Repositorio_Proyecto.objects.get(proyecto_id=pk, repositorio_id=repo['id'])
                except:

                    repositorio = Repositorio_Proyecto(proyecto_id=pk, repositorio_id=repo['id'],persona_id=request.user.username,nombre=repo['full_name']
                                                        ,link=repo['html_url'],propietario=repo['owner']['login'],contribuyentes_url=repo['contributors_url'])
                    repositorio.save()




        return Response(status=status.HTTP_200_OK)





class EstudianteMateriaList(APIView):

    def get(self, request, codigo_materia, format=None):
        personas_materia = Materia_Persona.objects.filter(materia__codigo=codigo_materia)
        serializer = Materia_PersonaSerializer(personas_materia, many=True)
        return Response(serializer.data)


class EstudianteProyectoList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, proyecto_id, format=None):
        estudiantes = Proyecto_Alumno.objects.filter(proyecto_id=proyecto_id)
        serializer = Proyecto_AlumnoSerializer(estudiantes,many=True)

        return Response(serializer.data)



class MateriaProyectoList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request, proyecto_id, format=None):
        materias = Materia_Proyecto.objects.filter(proyecto_id=proyecto_id)
        serializer = Materia_PersonaSerializer(materias,many=True)

        return Response(serializer.data)


class IdeaProyectoList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, proyecto_id, format=None):

        idea = Idea_Proyecto.objects.get(proyecto_id=proyecto_id)

        
        serializer = Idea_ProyectoSerializer(idea)


        return Response(serializer.data)

class RepostiroioProyectoList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, proyecto_id, format=None):
        repos = Repositorio_Proyecto.objects.filter(proyecto_id=proyecto_id)
        serializer = Repositorio_ProyectoSerializer(repos, many=True)

        return Response(serializer.data)
