from django.http import HttpResponse
from django.core.mail import EmailMessage

from rest_framework import status


class MailService:

    def welcome_mail(self, nombre, institucional, rol):
        if rol.nombre == "ESTUDIANTE":
            doc = open('templates/correos/bienvenida.html')
        else:
            doc = open('templates/correos/super_bienvenida.html')

        message = doc.read()

        content = message.replace('$name', nombre)

        email_message = EmailMessage(
            "Mensaje de bienvenida",
            content,
            "Mensajero de Teilen",
            [institucional],
        )

        email_message.content_subtype = 'html'
        email_message.send()

        return HttpResponse(status=status.HTTP_200_OK)
