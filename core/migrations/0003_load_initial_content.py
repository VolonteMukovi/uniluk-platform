"""Charge le contenu initial une seule fois, avec les migrations."""

from pathlib import Path

from django.db import migrations


def split_sql_statements(sql):
    """Découpe le fichier SQL sans couper les points-virgules dans les textes."""
    statements = []
    current = []
    quote = None
    escaped = False

    for character in sql:
        if quote:
            current.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
        elif character in ("'", '"'):
            quote = character
            current.append(character)
        elif character == ';':
            statement = ''.join(current).strip()
            if statement:
                statements.append(statement)
            current = []
        else:
            current.append(character)

    statement = ''.join(current).strip()
    if statement:
        statements.append(statement)
    return statements


def load_initial_content(apps, schema_editor):
    # Les données font partie de cette migration : Django ne rejoue jamais une
    # migration déjà appliquée, donc une base existante reste inchangée.
    seed_file = Path(__file__).resolve().parents[2] / 'database' / 'uniluk_seed.sql'
    sql = '\n'.join(
        line for line in seed_file.read_text(encoding='utf-8').splitlines()
        if not line.lstrip().startswith('--')
    )

    with schema_editor.connection.cursor() as cursor:
        for statement in split_sql_statements(sql):
            # Ces directives sont utiles dans le client mysql, mais inutiles ici.
            if statement.upper().startswith(('SET NAMES', 'SET FOREIGN_KEY_CHECKS')):
                continue
            cursor.execute(statement)


class Migration(migrations.Migration):
    dependencies = [('core', '0002_sitesettings_x_url')]

    operations = [migrations.RunPython(load_initial_content, migrations.RunPython.noop)]
