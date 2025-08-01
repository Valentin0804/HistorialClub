# Generated by Django 5.2 on 2025-04-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='arbitro',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='árbitro'),
        ),
        migrations.AddField(
            model_name='partido',
            name='instancia',
            field=models.CharField(choices=[('Fecha', 'Fecha'), ('RepIda', 'Repechaje Ida'), ('RepVue', 'Repechaje vuelta'), ('OctIda', 'Octavos ida'), ('OctVue', 'Octavos vuelta'), ('CuaIda', 'Cuartos ida'), ('CuaVue', 'Cuartos vuelta'), ('SemIda', 'Semi ida'), ('SemVue', 'Semi vuelta'), ('FinIda', 'Final ida'), ('FinVue', 'Final vuelta'), ('Rep', 'Repechaje'), ('Oct', 'Octavos'), ('Cua', 'Cuartos'), ('Semi', 'Semifinal'), ('Final', 'Final')], default='Fecha', max_length=6),
        ),
    ]
