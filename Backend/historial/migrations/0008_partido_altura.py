# Generated by Django 5.0.6 on 2025-07-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historial', '0007_alter_jugador_posicion'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='altura',
            field=models.CharField(choices=[('Ronda 1', 'Ronda 1'), ('Ronda 2', 'Ronda 2'), ('Playoff', 'Playoff'), ('No definido', 'ND')], default='No definido', max_length=20),
        ),
    ]
