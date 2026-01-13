import re
from django.db import models
from django.core.validators import MinValueValidator

class Club(models.Model):   # Rivales
    nombre = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    fundacion = models.DateField()
    escudo = models.CharField(max_length=100, null=True, blank=True)
    campeonatos = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    POSICIONES = [
        ('ARQ', 'Arquero'),
        ('DEF', 'Defensor'),
        ('MED', 'Mediocampista'),
        ('DEL', 'Delantero'),
        ('DT', 'Director Técnico'),
        ('SD', 'Sin Definir'),
    ]

    ESTADO_OPCIONES = [
        ('A', 'Activo'),
        ('R', 'Retirado'),
        ('T', 'Traspasado'),
    ]

    posicion = models.CharField(max_length=3, choices=POSICIONES)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='jugadores/', null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES, default='A')

    torneos = models.ManyToManyField('Torneo', through='ParticipacionJugador', blank=True)
    
    # Estadísticas generales (acumulativas)
    goles_totales = models.PositiveIntegerField(default=0)
    amarillas_totales = models.PositiveIntegerField(default=0)
    rojas_totales = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class ParticipacionJugador(models.Model):
    jugador = models.ForeignKey('Jugador', on_delete=models.CASCADE)
    torneo = models.ForeignKey('Torneo', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('jugador', 'torneo')

    def __str__(self):
        return f"{self.jugador} en {self.torneo}"

class Torneo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    Instancia = [
        ('Fecha', 'Fecha'),
        ('RepIda', 'Repechaje Ida'),
        ('RepVue', 'Repechaje vuelta'),
        ('OctIda', 'Octavos ida'),
        ('OctVue', 'Octavos vuelta'),
        ('CuaIda', 'Cuartos ida'),
        ('CuaVue', 'Cuartos vuelta'),
        ('SemIda', 'Semi ida'),
        ('SemVue', 'Semi vuelta'),
        ('FinIda', 'Final ida'),
        ('FinVue', 'Final vuelta'),
        ('Rep', 'Repechaje'),
        ('Oct', 'Octavos'),
        ('Cua', 'Cuartos'),
        ('Semi', 'Semifinal'),
        ('Final', 'Final'),
    ]

    TIPO = [('L', 'Local'), ('V', 'Visitante')]

    Altura = [
        ('Ronda 1', 'Ronda 1'),
        ('Ronda 2', 'Ronda 2'),
        ('Playoff', 'Playoff'),
        ('No definido', 'ND'),
    ]
    
    fecha = models.DateField(blank=True, null=True)
    torneo = models.ForeignKey(Torneo, on_delete=models.PROTECT)
    rival = models.ForeignKey(Club, on_delete=models.PROTECT)
    arbitro = models.CharField(max_length=100, blank=True, default="", verbose_name="árbitro")
    instancia = models.CharField(max_length=6, choices=Instancia, default="Fecha") 
    altura = models.CharField(max_length=20, choices=Altura, default="No definido") 
    tipo = models.CharField(max_length=1, choices=TIPO )
    goles_chabas = models.PositiveIntegerField(default=0)
    goles_rival = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)
    jugado = models.BooleanField(default=True, help_text="Marcar si el partido ya fue jugado")

    # Relaciones para estadísticas
    goleadores = models.ManyToManyField(
        Jugador, 
        through='Gol',
        related_name='goles_partidos'
    )
    amarillas = models.ManyToManyField(
        Jugador, 
        through='TarjetaAmarilla',
        related_name='amarillas_partidos'
    )
    rojas = models.ManyToManyField(
        Jugador, 
        through='TarjetaRoja',
        related_name='rojas_partidos'
    )

class Gol(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    minuto = models.PositiveIntegerField()

class TarjetaAmarilla(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    minuto = models.PositiveIntegerField()

class TarjetaRoja(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    minuto = models.PositiveIntegerField()

class VideoPartido(models.Model):

    CLASIFICACION_CHOICES = [
        ('Completo', 'Partido Completo'),
        ('Resumen', 'Resumen'),
        ('Goles', 'Goles'), # Puedes agregar más clasificaciones como "Goles" o "Momentos destacados"
        ('Otros', 'Otros'),
    ]

    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='videos')
    url_youtube = models.URLField(max_length=200, help_text="URL del video de YouTube")
    clasificacion = models.CharField(
        max_length=10, 
        choices=CLASIFICACION_CHOICES, 
        default='Resumen',
        help_text="Clasificación del video (ej. Partido Completo, Resumen)"
    )
    titulo = models.CharField(max_length=200, blank=True, null=True, help_text="Título opcional para el video")

    def get_youtube_id(self):
        youtube_regex = (
            r'(?:https?://)?(?:www\.)?'
            r'(?:youtube\.com|youtu\.be)/'
            r'(?:watch\?v=|embed/|v/|)'
            r'([\w-]{11})'
        )
        match = re.search(youtube_regex, self.url_youtube)
        if match:
            return match.group(1)
        return None 

    def __str__(self):
        return f"Video de {self.clasificacion} para {self.partido}"
    
class HitoHistorico(models.Model):
    TIPO_CHOICES = [
        ('fundacion', 'Fundación'),
        ('cancha', 'Cancha'),
        ('partido', 'Partido histórico'),
        ('campeonato', 'Campeonato'),
        ('otro', 'Otro'),
    ]

    fecha = models.DateField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    partido = models.ForeignKey(
        Partido,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Partido relacionado (si aplica)"
    )

    imagen = models.ImageField(upload_to='hitos/', blank=True, null=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"{self.fecha} - {self.titulo}"
