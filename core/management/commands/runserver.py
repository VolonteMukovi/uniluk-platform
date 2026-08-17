"""Démarre le serveur après avoir appliqué les migrations nécessaires."""

from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.management.commands.runserver import Command as DjangoRunserverCommand


class Command(DjangoRunserverCommand):
    help = (
        'Démarre le serveur de développement après la création automatique des '
        'tables et le chargement initial des données.'
    )

    def handle(self, *args, **options):
        call_command(
            'migrate',
            interactive=False,
            verbosity=options.get('verbosity', 1),
        )
        # `runserver` est uniquement destiné au développement : sert également
        # les fichiers statiques lorsque DJANGO_DEBUG=False dans le fichier .env.
        if not settings.DEBUG:
            options['insecure'] = True
        return super().handle(*args, **options)
