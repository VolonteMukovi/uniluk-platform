from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='x_url',
            field=models.URLField(blank=True, verbose_name='Lien X / Twitter'),
        ),
    ]
