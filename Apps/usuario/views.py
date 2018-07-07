import requests
import json

from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import (
    Http404, JsonResponse, HttpResponse
)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from Apps.usuario.models import (
    Usuario, Persona, GithubPersona
)
from Apps.usuario.serializers import PersonaSerializer
from Apps.principal.models import (
    Materia, Materia_Persona, Proyecto, Materia_Proyecto, Proyecto_Alumno
)
from Apps.principal.serializers import (
    Materia_PersonaSerializer, Proyecto_AlumnoSerializer, ProyectoSerializer
)

from Teilen.Modules.services import SessionsService
from Teilen.Modules.github import Github

session = SessionsService()


class SesionDocente(APIView):
    """Crea la sesión y retorna un Token de conexión para docentes.

    Realiza la consulta al emulador de Divisist y con la información recibida
    registra un nuevo usuario para docente y retorna un token de conexión.

    Si es la primera vez que se realiza la conexión enviará
    un correo de bienvenida al docente.

    Para conocer más consulte Teilen.Modules (services o email)

    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        codigo = request.data['code']
        documento = request.data['doc']
        password = request.data['pass']

        data = {
            'code': codigo,
            'doc': documento,
            'pass': password
        }

        r = requests.post(
            "http://localhost:8080/usuario/docente/",
            data=data
        )

        try:
            docente = json.loads(r.text)

            token = session.create_session(usuario=docente)

            return JsonResponse(token)
        except:
            if r.status_code == 401:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if r.status_code == 404:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SesionEstudiante(APIView):
    """Crea la sesión y retorna un Token de conexión para estudiantes.

    Realiza la consulta al emulador de Divisist y con la información recibida
    registra un nuevo usuario para estudiante y retorna un token de conexión.

    Si es la primera vez que se realiza la conexión enviará
    un correo de bienvenida al estudiante.

    Para conocer más consulte Teilen.Modules (services o email)

    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        codigo = request.data['code']
        documento = request.data['doc']
        password = request.data['pass']

        data = {
            'code': codigo,
            'doc': documento,
            'pass': password
        }

        r = requests.post(
            "http://localhost:8080/usuario/estudiante/",
            data=data
        )

        try:

            estudiante = json.loads(r.text)
            token = session.create_session(usuario=estudiante)
            return JsonResponse(token)

        except  Exception as  e :
            print(e)
            if r.status_code == 401:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if r.status_code == 404:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class EstudianteList(APIView):
    """Retorna un listado de todos los estudiantes.

    Consulta, serializa y retorna un listado con todas las personas con
    rol estudiante

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        personas = Persona.objects.filter(rol__nombre="ESTUDIANTE")
        serializer = PersonaSerializer(personas, many=True)

        return Response(serializer.data)


class PersonaDetail(APIView):
    """Obtiene la información de la persona con sesión activa.

    Basándose en la información de la sesión la función get
    obtiene los datos de la persona, los serializa y los retorna

    """
    parser_classes = (JSONParser,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        persona = self.get_object(request.user.username)

        serializer = PersonaSerializer(persona)

        return Response(serializer.data)


class MateriaList(APIView):
    """Lista las materias matriculadas de una persona.

    Bajo la función get obtiene un listado con las materias matriculadas
    por una persona

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        persona = Persona.objects.get(codigo=request.user.username)

        materias_personas = Materia_Persona.objects.filter(
            persona__codigo=request.user.username,
            fecha_creacion__year=persona.año_actual.year,
            semestre=persona.semestre_actual
        )

        serializer = Materia_PersonaSerializer(materias_personas, many=True)

        return Response(serializer.data)


class ProyectList(APIView):
    """Lista mis proyectos como alumno

    Retorna un listado de proyectos a los que un alumno ha sido asignado

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        proyectos = Proyecto_Alumno.objects.filter(alumno_id=request.user.persona.codigo)

        serializer = Proyecto_AlumnoSerializer(proyectos,many=True)

        return Response(serializer.data)



class GithubMiddleware(APIView):
    parser_classes = (JSONParser,)


    def post(self, request, format=None):

        codigo = request.data['codigo']

        headers = { 'Accept':'application/json'}


        data = "client_id=1a9db4bc7d429c820f19&client_secret=a1781050f898fe9e161c06c9fd81d605836a01ab&code="+codigo

        respuesta = requests.post('https://github.com/login/oauth/access_token',data=data,headers=headers)

        try:

            token = respuesta.json()['access_token']
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:

            githubpersona = GithubPersona.objects.get(persona_id=request.user.username)
            githubpersona.token=token
            githubpersona.save()
        except:
            githubpersona = GithubPersona(persona_id=request.user.username, token=token)
            githubpersona.save()






        repos = Github.listarRepos(token)
        return Response(repos)





class RepositoriosGithubList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request, format=None):

        try:

            githubpersona = GithubPersona.objects.get(persona_id=request.user.username)
            repos = Github.listarRepos(githubpersona.token)
            return Response(repos)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProyectoDocenteList(APIView):
    """Lista mis proyectos como docente

    Retorna el listado de proyectos que el docente con la sesión activa ha creado

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        proyectos = Proyecto.objects.filter(docente_id=request.user.username)
        serializer = ProyectoSerializer(proyectos,many=True)

        return Response(serializer.data)

