from django.db import migrations, models


def populate_about_content(apps, schema_editor):
    PageContent = apps.get_model('core', 'PageContent')
    about = PageContent.objects.filter(key='about').first()
    if not about:
        return

    # La fiche créée par la migration précédente reçoit les textes complets.
    # Une fiche déjà personnalisée par un administrateur est conservée telle quelle.
    if about.title == 'À propos de l’UNILUK' and about.content == 'Image de la section À propos.':
        about.title = 'Une communauté d’apprentissage fondée sur l’excellence et le caractère'
        about.subtitle = 'À propos de l’UNILUK'
        about.content = (
            'Née de la vision de l’Église Adventiste du Septième Jour, l’UNILUK forme '
            'des cadres compétents dans les domaines de la théologie, de la gestion, de '
            'la santé, de l’éducation et des techniques appliquées. Notre pédagogie associe '
            'rigueur scientifique, encadrement personnalisé et développement du caractère.'
        )
    about.highlight_value = '30+'
    about.highlight_label = 'années au service de la formation à Lukanga'
    about.save()


class Migration(migrations.Migration):
    dependencies = [('core', '0004_add_about_page_content')]

    operations = [
        migrations.AddField(
            model_name='pagecontent',
            name='highlight_value',
            field=models.CharField(blank=True, max_length=50, verbose_name='Valeur mise en avant'),
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='highlight_label',
            field=models.CharField(blank=True, max_length=255, verbose_name='Libellé de la mise en avant'),
        ),
        migrations.RunPython(populate_about_content, migrations.RunPython.noop),
    ]
