from django.db import migrations


def add_about_page_content(apps, schema_editor):
    PageContent = apps.get_model('core', 'PageContent')
    PageContent.objects.get_or_create(
        key='about',
        defaults={
            'title': 'À propos de l’UNILUK',
            'content': 'Image de la section À propos.',
            'image_url': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=900&q=80',
        },
    )


class Migration(migrations.Migration):
    dependencies = [('core', '0003_load_initial_content')]

    operations = [migrations.RunPython(add_about_page_content, migrations.RunPython.noop)]
