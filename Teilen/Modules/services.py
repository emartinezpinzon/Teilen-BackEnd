"""Service agrupa clases y funciones que sirven de auxiliar al API.

"""

from rest_framework.authtoken.models import Token

from Apps.usuario.models import (
    Usuario, Persona, Rol
)

from Apps.principal.models import (
    Materia, Materia_Persona
)

from Teilen.Modules.email import MailService

class SessionsService:
    """Crea una sesión para un usuario en TeiLen.

    Esta clase permite crear una sesión para un usuario en TeiLen,
    las peticiones que recibe el API para el inicio de sesión son apoyadas
    por este servicio, quien regresa un Token de conexión

    """

    def create_session(self, **args):
        """Crea y retorna un token de sesión.

        Esta función realiza varias comprobaciones e invoca otras funciones
        auxiliares para generar un Token de sesión que pueda retornar

        """
        usuario = args["usuario"]

        if not Usuario.objects.filter(username=usuario["codigo"]).exists():
            user = self.__create_user(usuario=usuario)
        else:
            user = self.__update_user(usuario=usuario)

        if not Persona.objects.filter(codigo=usuario["codigo"]).exists():
            person = self.__create_person(user, usuario=usuario)
        else:
            if Persona.objects.filter(rol__nombre=usuario["rol"].upper()).exists():
                person = self.__update_person(usuario=usuario)
            else:
                person = self.__create_person(user, usuario=usuario)


        self.__load_courses(usuario=usuario)

        return self.__login(usuario=usuario)

    def __get_role(self, name):
        """Obtiene el rol del usuario.

        En principio esta función trata de obtener el rol del usuario,
        sin embargo, si el rol no se encuentra registrado hace su creación

        En cualquier caso va a retornar un objeto de tipo Rol
        con el nombre que se le ha pasado en parámetro en mayúscula

        """
        role = name.upper()

        try:
            rol = Rol.objects.get(nombre=role)
        except Rol.DoesNotExist:
            rol = Rol(nombre=role)
            rol.save()

        return rol

    def __create_user(self, **args):
        """Crea un usuario en el modelo usuario.Usuario.

        En caso de no existir un usuario, esta función lo crea para seguir
        con el establecimiento de la sesión

        """
        usuario = args["usuario"]

        user = Usuario.objects.create_user(
            usuario["codigo"],
            usuario["correo"],
            first_name=usuario["nombre"],
            last_name=usuario["apellido"],
            email_institucional=usuario["correo_institucional"],
            documento=usuario["documento"],
            imagen=usuario["imagen"],
            telefono=usuario["celular"]
        )
        user.save()

        return user

    def __update_user(self, **args):
        """Actualiza la información del usuario.

        Si existe el usuario realiza una actualización de datos para evitar
        diferencias entre el proveedor en Divisist y los datos locales

        """
        usuario = args["usuario"]

        user = Usuario.objects.get(username=usuario["codigo"])
        user.email = usuario["correo"]
        user.first_name = usuario["nombre"]
        user.last_name = usuario["apellido"]
        user.email_institucional = usuario["correo_institucional"]
        user.documento = usuario["documento"]
        user.imagen = usuario["imagen"]
        user.telefono = usuario["celular"]
        user.save()

        return user

    def __create_person(self, user, **args):
        """Crea un registro en usuario.Persona para un usuario existente

        """

        usuario = args["usuario"]

        rol = self.__get_role(usuario["rol"])

        person = Persona(
            codigo=usuario["codigo"],
            carrera=usuario["carrera"],
            semestre_actual=usuario["semestre_actual"],
            año_actual=usuario["año_actual"],
            persona=user,
            rol=rol
        )
        person.save()

        email = MailService()
        email.welcome_mail(user.first_name, user.email_institucional, rol)

        return person

    def __update_person(self, **args):
        """Actualiza un registro de persona existente.

        Hace una actualización de los datos de persona guardados localmente
        comparados con los datos que provee divisist

        """
        usuario = args["usuario"]

        person = Persona.objects.get(codigo=usuario["codigo"])
        person.carrera = usuario["carrera"]
        person.semestre_actual = usuario["semestre_actual"]
        person.año_actual = usuario["año_actual"]
        person.save()

        return person

    def __login(self, **args):
        """Establece una sesión mediante un Token de usuario.

        Obtiene un Token de acceso que sirve como conexión de
        una sesión para comunicarse con el API

        """

        usuario = args["usuario"]

        user = Usuario.objects.get(username=usuario["codigo"])

        try:
            token = Token.objects.create(user=user)
        except:
            token = Token.objects.get(user=user)

        data = {
            'token': token.key,
            'codigo': usuario["codigo"],
            'nombre': usuario["nombre"],
            'apellido': usuario["apellido"],
            'imagen': usuario["imagen"],
            'rol': usuario["rol"]
        }

        return data

    def __load_courses(self, **args):
        """Carga los cursos matriculados del usuario.

        Lee, registra y/o carga los cursos matriculados por el usuario con sus
        respectivos años y semestres

        """
        usuario = args["usuario"]
        materias = usuario["materias"]

        for codigo in materias.keys():
            if not Materia.objects.filter(codigo=codigo).exists():
                materia = Materia(
                    codigo,
                    materias[codigo]
                )
                materia.save()

            if not Materia_Persona.objects.filter(materia_id=codigo).filter(persona_id=usuario["codigo"]).filter(semestre=usuario["semestre_actual"]).exists():
                mp = Materia_Persona(
                    materia_id=codigo,
                    persona_id=usuario["codigo"],
                    semestre=usuario["semestre_actual"]
                )
                mp.save()
