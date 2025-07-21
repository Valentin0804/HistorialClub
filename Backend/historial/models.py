from django.db import models
from django.core.validators import MinValueValidator

class Club(models.Model):   # Rivales
    nombre = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    fundacion = models.DateField()
    escudo = models.ImageField(upload_to='escudos/', null=True, blank=True)
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
    
    fecha = models.DateField(blank=True, null=True)
    torneo = models.ForeignKey(Torneo, on_delete=models.PROTECT)
    rival = models.ForeignKey(Club, on_delete=models.PROTECT)
    arbitro = models.CharField(max_length=100, blank=True, default="", verbose_name="árbitro")
    instancia = models.CharField(max_length=6, choices=Instancia, default="Fecha") 
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