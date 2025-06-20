from django.shortcuts import render, get_object_or_404
from .models import Partido, Jugador, Club, Gol, TarjetaAmarilla, TarjetaRoja, Torneo
from django.db.models import Count, F, Sum


def home(request):
    # Obtener estadísticas para la portada
    partidos_count = Partido.objects.count()
    titulos_count = 12  # Reemplaza con tu modelo real si lo tienes
    jugadores_count = Jugador.objects.count()
    
    # Obtener último partido jugado
    ultimo_partido = Partido.objects.select_related('rival', 'torneo').order_by('-fecha').first()
    
    return render(request, 'historial/home.html', {
        'partidos_count': partidos_count,
        'titulos_count': titulos_count,
        'jugadores_count': jugadores_count,
        'ultimo_partido': ultimo_partido
    })

def lista_partidos(request):
    """Muestra todos los partidos ordenados por fecha descendente"""
    partidos = Partido.objects.all().order_by('-fecha')
    return render(request, 'historial/lista_partidos.html', {'partidos': partidos})

def detalle_partido(request, partido_id):
    partido = get_object_or_404(
        Partido.objects.select_related('torneo', 'rival')
        .prefetch_related(
            'gol_set__jugador',
            'tarjetaamarilla_set__jugador',
            'tarjetaroja_set__jugador'
        ), 
        pk=partido_id
    )
    return render(request, 'historial/detalle_partido.html', {
        'partido': partido,
        'goles': partido.gol_set.all().order_by('minuto'),
        'amarillas': partido.tarjetaamarilla_set.all().order_by('minuto'),
        'rojas': partido.tarjetaroja_set.all().order_by('minuto')
    })

def temporada_actual(request):
    # Obtener el nombre del último torneo
    ultimo_torneo_nombre = Torneo.objects.order_by('-fecha_fin').values_list('nombre', flat=True).first()
    
    partidos = Partido.objects.filter(
        torneo__nombre=ultimo_torneo_nombre
    ).order_by('fecha')
    
    return render(request, 'historial/temporada_actual.html', {
        'partidos': partidos,
        'temporada_actual': ultimo_torneo_nombre or "No hay torneos"
    })

def historicos(request):
    temporadas = Torneo.objects.values_list('nombre', flat=True).distinct()
    equipos = Club.objects.all()
    
    # Filtros
    temporada_seleccionada = request.GET.get('temporada')
    equipo_seleccionado = request.GET.get('equipo')
    
    partidos = Partido.objects.all()
    
    if temporada_seleccionada:
        partidos = partidos.filter(torneo__nombre=temporada_seleccionada)
    
    if equipo_seleccionado:
        partidos = partidos.filter(rival__id=equipo_seleccionado)
    
     # Estadísticas base
    total_partidos = partidos.count()
    total_goles_a_favor = partidos.aggregate(total=Sum('goles_chabas'))['total'] or 0
    total_goles_en_contra = partidos.aggregate(total=Sum('goles_rival'))['total'] or 0
    total_amarillas = TarjetaAmarilla.objects.filter(partido__in=partidos).count()
    total_rojas = TarjetaRoja.objects.filter(partido__in=partidos).count()

    # Conteo de resultados
    victorias = partidos.filter(goles_chabas__gt=F('goles_rival')).count()
    derrotas = partidos.filter(goles_chabas__lt=F('goles_rival')).count()
    empates = partidos.filter(goles_chabas=F('goles_rival')).count()

    vallas_invictas = partidos.filter(goles_rival=0).count()
    
    # Cálculo de rachas
    partidos_ordenados = partidos.order_by('fecha')
    racha_actual_no_perdidos = 0
    max_racha_no_perdidos = 0
    racha_actual_ganados = 0
    max_racha_ganados = 0
    
    for partido in partidos_ordenados:
        # Cálculo racha no perdidos (victorias o empates)
        if partido.goles_chabas >= partido.goles_rival:
            racha_actual_no_perdidos += 1
            if racha_actual_no_perdidos > max_racha_no_perdidos:
                max_racha_no_perdidos = racha_actual_no_perdidos
        else:
            racha_actual_no_perdidos = 0
            
        # Cálculo racha ganados
        if partido.goles_chabas > partido.goles_rival:
            racha_actual_ganados += 1
            if racha_actual_ganados > max_racha_ganados:
                max_racha_ganados = racha_actual_ganados
        else:
            racha_actual_ganados = 0
    
    # Porcentajes de rendimiento
    porcentaje_victorias = (victorias / total_partidos * 100) if total_partidos > 0 else 0
    promedio_goles_favor = (total_goles_a_favor / total_partidos) if total_partidos > 0 else 0
    promedio_goles_contra = (total_goles_en_contra / total_partidos) if total_partidos > 0 else 0

    estadisticas = {
        'partidos': total_partidos,
        'goles_a_favor': total_goles_a_favor,
        'goles_en_contra': total_goles_en_contra,
        'victorias': victorias,
        'derrotas': derrotas,
        'empates': empates,
        'amarillas': total_amarillas,
        'rojas': total_rojas,
        'vallas_invictas': vallas_invictas,
        'porcentaje_victorias': round(porcentaje_victorias, 2),
        'max_racha_no_perdidos': max_racha_no_perdidos,
        'promedio_goles_favor': round(promedio_goles_favor, 2),
        'promedio_goles_contra': round(promedio_goles_contra, 2),
    }

    return render(request, 'historial/historicos.html', {
        'partidos': partidos.order_by('-fecha'),
        'temporadas': temporadas,
        'equipos': equipos,
        'filtros': {
            'temporada': temporada_seleccionada,
            'equipo': equipo_seleccionado
        },
        'estadisticas': estadisticas
    })

def estadisticas(request):
    jugadores = Jugador.objects.all()
    temporadas = Torneo.objects.values_list('nombre', flat=True).distinct()
    equipos = Club.objects.all()
    
    # Filtros
    temporada_seleccionada = request.GET.get('temporada')
    jugador_seleccionado = request.GET.get('jugador')
    equipo_seleccionado = request.GET.get('equipo')
    
    # Consulta base con filtros aplicados correctamente
    queryset_goles = Jugador.objects.all()
    queryset_amarillas = Jugador.objects.all()
    queryset_rojas = Jugador.objects.all()
    
    # Aplicar filtros a cada queryset
    if temporada_seleccionada:
        queryset_goles = queryset_goles.filter(
            gol__partido__torneo__nombre=temporada_seleccionada
        ).distinct()
        queryset_amarillas = queryset_amarillas.filter(
            tarjetaamarilla__partido__torneo__nombre=temporada_seleccionada
        ).distinct()
        queryset_rojas = queryset_rojas.filter(
            tarjetaroja__partido__torneo__nombre=temporada_seleccionada
        ).distinct()
    
    if jugador_seleccionado:
        queryset_goles = queryset_goles.filter(id=jugador_seleccionado)
        queryset_amarillas = queryset_amarillas.filter(id=jugador_seleccionado)
        queryset_rojas = queryset_rojas.filter(id=jugador_seleccionado)
    
    if equipo_seleccionado:
        queryset_goles = queryset_goles.filter(
            gol__partido__rival__id=equipo_seleccionado
        ).distinct()
        queryset_amarillas = queryset_amarillas.filter(
            tarjetaamarilla__partido__rival__id=equipo_seleccionado
        ).distinct()
        queryset_rojas = queryset_rojas.filter(
            tarjetaroja__partido__rival__id=equipo_seleccionado
        ).distinct()
    
    # Anotar los conteos después de aplicar los filtros
    estadisticas_data = {
        'goleadores': queryset_goles.annotate(total_goles=Count('gol', distinct=True)),
        'amarillas': queryset_amarillas.annotate(total_amarillas=Count('tarjetaamarilla', distinct=True)),
        'rojas': queryset_rojas.annotate(total_rojas=Count('tarjetaroja', distinct=True))
    }
    
    return render(request, 'historial/estadisticas.html', {
        'estadisticas': estadisticas_data,
        'jugadores': jugadores,
        'temporadas': temporadas,
        'equipos': equipos,
        'filtros': {
            'temporada': temporada_seleccionada,
            'jugador': jugador_seleccionado,
            'equipo': equipo_seleccionado
        }
    })

def rivales(request):
    clubes = Club.objects.all()

    data = []

    for club in clubes:
        partidos = Partido.objects.filter(rival=club)

        ganados = partidos.filter(goles_chabas__gt=F('goles_rival')).count()
        empatados = partidos.filter(goles_chabas=F('goles_rival')).count()
        perdidos = partidos.filter(goles_chabas__lt=F('goles_rival')).count()

        data.append({
            'nombre': club.nombre,
            'fundacion': club.fundacion,
            'campeonatos': club.campeonatos,
            'escudo': club.escudo.url if club.escudo else None,
            'ganados': ganados,
            'empatados': empatados,
            'perdidos': perdidos,
        })

    return render(request, 'historial/rivales.html', {'clubes': data})
