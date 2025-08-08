# tu_app/management/commands/backup_futbol.py

import json
import csv
import os
from datetime import datetime, date 

from django.core.management.base import BaseCommand
from django.core import serializers
from django.apps import apps
from django.db import transaction, models

# Asegúrate de reemplazar 'tu_app' con el nombre real de tu aplicación de Django
# donde tienes definidos los modelos.
from historial.models import (
    Club, Jugador, Torneo, ParticipacionJugador,
    Partido, Gol, TarjetaAmarilla, TarjetaRoja
)

# --- Instrucciones de Uso ---
#
# Para crear una copia de seguridad:
# python manage.py backup_restore --backup
#
# Para restaurar una copia de seguridad (asegúrate de que la base de datos esté vacía o preparada):
# python manage.py backup_restore --restore --filepath backups/backup_futbol_20250805_232559.json
#
# Para crear un archivo CSV con las estadísticas de los jugadores:
# python manage.py backup_futbol --export-csv
#
def json_serial(obj):
    """Serializador de JSON para objetos que no son serializables por defecto."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat() # Convierte la fecha/hora a formato "AAAA-MM-DDTHH:MM:SS" o "AAAA-MM-DD"
    raise TypeError(f"El tipo {type(obj)} no es serializable en JSON")


class Command(BaseCommand):
    help = 'Realiza copias de seguridad, restaura y exporta datos de la aplicación de fútbol.'

    def add_arguments(self, parser):
        parser.add_argument('--backup', action='store_true', help='Crear una copia de seguridad de los datos.')
        parser.add_argument('--restore', action='store_true', help='Restaurar datos desde una copia de seguridad.')
        parser.add_argument('--filepath', type=str, help='Ruta del archivo de copia de seguridad para la restauración.')
        parser.add_argument('--export-csv', action='store_true', help='Exportar estadísticas de jugadores a un archivo CSV.')

    def handle(self, *args, **options):
        if options['backup']:
            self.backup_data()
        elif options['restore']:
            filepath = options['filepath']
            if filepath:
                self.restore_data(filepath)
            else:
                self.stdout.write(self.style.ERROR("Por favor, especifica la ruta del archivo de respaldo con --filepath"))
        elif options['export_csv']:
            self.export_jugadores_to_csv()
        else:
            self.stdout.write("Por favor, especifica una acción: --backup, --restore, o --export-csv")

    def backup_data(self):
        """
        Crea una copia de seguridad de los modelos en un archivo JSON.
        Los campos de imagen (escudo, foto) se omiten.
        """
        self.stdout.write("Iniciando copia de seguridad...")

        # Orden correcto para evitar problemas de dependencias
        models_to_backup = [
            'Torneo', 'Club', 'Jugador', 'ParticipacionJugador',
            'Partido', 'Gol', 'TarjetaAmarilla', 'TarjetaRoja'
        ]
        
        backup_data = {}

        for model_name in models_to_backup:
            model = apps.get_model('historial', model_name)
            data = serializers.serialize('python', model.objects.all())
            
            for item in data:
                if 'escudo' in item['fields']:
                    item['fields']['escudo'] = ''
                if 'foto' in item['fields']:
                    item['fields']['foto'] = ''
            
            backup_data[model_name] = data
            self.stdout.write(f"Respaldados {len(data)} objetos de {model_name}")

        # Crear el directorio de backups si no existe
        os.makedirs('backups', exist_ok=True)
        
        filename = f'backup_futbol_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        filepath = os.path.join('backups', filename)

        with open(filepath, 'w', encoding='utf-8') as f:
             json.dump(backup_data, f, indent=4, ensure_ascii=False, default=json_serial)

        self.stdout.write(self.style.SUCCESS(f"Copia de seguridad creada exitosamente en {filepath}"))

    @transaction.atomic
    def restore_data(self, filepath):
        """
        Restaura los datos desde un archivo JSON a la base de datos.
        """
        self.stdout.write(self.style.WARNING(f"Iniciando restauración desde {filepath}"))
        self.stdout.write(self.style.WARNING("ADVERTENCIA: Se recomienda ejecutar esto en una base de datos limpia para evitar conflictos de ID."))

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: No se encontró el archivo en la ruta {filepath}"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error: El archivo de respaldo no es un JSON válido."))
            return

        # El mismo orden que en el backup para restaurar correctamente las dependencias
        restore_order = [
            'Torneo', 'Club', 'Jugador', 'ParticipacionJugador',
            'Partido', 'Gol', 'TarjetaAmarilla', 'TarjetaRoja'
        ]

        with transaction.atomic():
            for model_name in restore_order:
                if model_name in backup_data:
                    model_data = backup_data[model_name]
                    model = apps.get_model('historial', model_name)
                    for item in model_data:
                        for field_name, value in item['fields'].items():
                            if value is None:
                                continue
                            try:
                                field = model._meta.get_field(field_name)
                                if isinstance(field, (models.DateField, models.DateTimeField)):
                                    # Convertir desde el formato ISO que guardamos
                                    if isinstance(field, models.DateTimeField):
                                        item['fields'][field_name] = datetime.fromisoformat(value)
                                    else:
                                        item['fields'][field_name] = date.fromisoformat(value)
                            except (models.fields.FieldDoesNotExist, AttributeError):
                                pass # Ignorar si no es un campo directo del modelo (ej. relaciones)

                    try:
                        for obj in serializers.deserialize('python', model_data):
                            obj.save()
                        self.stdout.write(f"Restaurados {len(model_data)} objetos de {model_name}")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error restaurando el modelo {model_name}: {e}"))
                        raise

        self.stdout.write(self.style.SUCCESS("Restauración completada exitosamente."))

    def export_jugadores_to_csv(self):
        """
        Exporta los jugadores y sus estadísticas a un archivo CSV.
        """
        self.stdout.write("Iniciando exportación de jugadores a CSV...")
        
        # Crear el directorio de exports si no existe
        os.makedirs('exports', exist_ok=True)

        csv_filename = f'estadisticas_jugadores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        csv_filepath = os.path.join('exports', csv_filename)

        # Encabezados del archivo CSV
        headers = ['ID', 'Nombre', 'Apellido', 'Posicion', 'Goles Totales', 'Amarillas Totales', 'Rojas Totales']

        try:
            with open(csv_filepath, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(headers)
                
                # Obtener todos los jugadores y escribir sus datos
                for jugador in Jugador.objects.all():
                    writer.writerow([
                        jugador.id,
                        jugador.nombre,
                        jugador.apellido,
                        jugador.get_posicion_display(),  # Muestra el nombre completo de la posición
                        jugador.goles_totales,
                        jugador.amarillas_totales,
                        jugador.rojas_totales
                    ])
            
            self.stdout.write(self.style.SUCCESS(f"Archivo CSV generado exitosamente en: {csv_filepath}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocurrió un error al generar el CSV: {e}"))