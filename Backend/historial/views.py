from django.shortcuts import render, get_object_or_404
from .models import Partido, Jugador, Club, Gol, TarjetaAmarilla, TarjetaRoja, Torneo
from django.db.models import Count, F, Func, Q
from django.utils import timezone

def home(request):
    # Obtener estadísticas para la portada
    partidos_count = Partido.objects.count()
    titulos_count = 12  # Reemplaza con tu modelo real si lo tienes
    jugadores_count = Jugador.objects.count()
    
    # Último partido jugado
    ultimo_partido = Partido.objects.select_related('rival', 'torneo')\
        .filter(jugado=True)\
        .order_by('-fecha')\
        .first()
    
    # Próximo partido (aún no jugado)
    proximo_partido = Partido.objects.select_related('rival', 'torneo')\
        .filter(jugado=False)\
        .order_by('fecha')\
        .first()

    # Máxima goleada
    maxima_goleada = Partido.objects.filter(
        goles_chabas__gt=F('goles_rival')
    ).annotate(
        diferencia_goles=F('goles_chabas') - F('goles_rival')
    ).order_by('-diferencia_goles').first()
    
    return render(request, 'historial/home.html', {
        'partidos_count': partidos_count,
        'titulos_count': titulos_count,
        'jugadores_count': jugadores_count,
        'ultimo_partido': ultimo_partido,
        'proximo_partido': proximo_partido,
        'maxima_goleada': maxima_goleada,
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
        'rojas': partido.tarjetaroja_set.all().order_by('minuto'),
        'arbitro': partido.arbitro if partido.arbitro else None,
        'instancia': partido.get_instancia_display(),
        'descripcion': partido.descripcion
    })

def temporada_actual(request):
    # Obtener el año actual
    año_actual = timezone.now().year

    # Filtrar partidos cuya fecha sea en el año actual

    partidos = Partido.objects.filter(
        fecha__year=año_actual, jugado=True
    ).order_by('fecha')

    return render(request, 'historial/temporada_actual.html', {
        'partidos': partidos,
        'temporada_actual': f"Temporada {año_actual}"
    })

def historicos(request):
    # Filtros y opciones
    años_disponibles = Partido.objects.dates('fecha', 'year', order='DESC')
    equipos = Club.objects.all()
    temporadas = Torneo.objects.values_list('nombre', flat=True).distinct()
    partidos_disponibles = Partido.objects.order_by('-fecha')
    jugadores = Jugador.objects.all()

    # Filtros GET
    temporada_seleccionada = request.GET.get('temporada')
    equipo_seleccionado = request.GET.get('equipo')
    año_seleccionado = request.GET.get('anio')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    ultimos_n = request.GET.get('ultimos')
    desde_partido_id = request.GET.get('desde_partido')
    jugador_id = request.GET.get('jugador')
    accion = request.GET.get('accion')  # 'gol', 'amarilla', 'roja'

    # Aplicar filtros
    partidos = Partido.objects.filter(jugado=True)

    if temporada_seleccionada:
        partidos = partidos.filter(torneo__nombre=temporada_seleccionada)

    if año_seleccionado and año_seleccionado.isdigit():
        partidos = partidos.filter(fecha__year=int(año_seleccionado))

    if equipo_seleccionado and equipo_seleccionado.isdigit():
        partidos = partidos.filter(rival__id=int(equipo_seleccionado))

    if fecha_desde:
        partidos = partidos.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        partidos = partidos.filter(fecha__lte=fecha_hasta)

    if desde_partido_id and desde_partido_id.isdigit():
        partido_ref = Partido.objects.filter(id=int(desde_partido_id)).first()
        if partido_ref:
            partidos = partidos.filter(fecha__gte=partido_ref.fecha)

    if jugador_id and jugador_id.isdigit():
        jugador_id = int(jugador_id)
        if accion == 'gol':
            partidos_ids_con_gol = Gol.objects.filter(jugador_id=jugador_id).values_list('partido_id', flat=True)
            partidos = partidos.filter(id__in=partidos_ids_con_gol)
        elif accion == 'amarilla':
            partidos_ids_con_amarilla = TarjetaAmarilla.objects.filter(jugador_id=jugador_id).values_list('partido_id', flat=True)
            partidos = partidos.filter(id__in=partidos_ids_con_amarilla)
        elif accion == 'roja':
            partidos_ids_con_roja = TarjetaRoja.objects.filter(jugador_id=jugador_id).values_list('partido_id', flat=True)
            partidos = partidos.filter(id__in=partidos_ids_con_roja)


    # Ordenamos por fecha descendente antes del corte
    partidos_filtrados = partidos.order_by('-fecha')

    # Si se pidieron los últimos N partidos, se aplica después del resto de filtros
    if ultimos_n and ultimos_n.isdigit():
        partidos_mostrados = list(partidos_filtrados[:int(ultimos_n)])
    else:
        partidos_mostrados = list(partidos_filtrados)

    # Estadísticas (solo de los partidos mostrados)
    total_partidos = len(partidos_mostrados)
    total_goles_a_favor = sum(p.goles_chabas for p in partidos_mostrados)
    total_goles_en_contra = sum(p.goles_rival for p in partidos_mostrados)

    partidos_ids = [p.id for p in partidos_mostrados]
    total_amarillas = TarjetaAmarilla.objects.filter(partido_id__in=partidos_ids).count()
    total_rojas = TarjetaRoja.objects.filter(partido_id__in=partidos_ids).count()

    victorias = sum(1 for p in partidos_mostrados if p.goles_chabas > p.goles_rival)
    empates = sum(1 for p in partidos_mostrados if p.goles_chabas == p.goles_rival)
    derrotas = sum(1 for p in partidos_mostrados if p.goles_chabas < p.goles_rival)
    vallas_invictas = sum(1 for p in partidos_mostrados if p.goles_rival == 0)

    # Cálculo de rachas (en orden cronológico)
    partidos_ordenados = sorted(
    [p for p in partidos_mostrados if p.fecha is not None],
    key=lambda p: p.fecha)
    racha_actual_no_perdidos = 0
    max_racha_no_perdidos = 0
    racha_actual_ganados = 0
    max_racha_ganados = 0

    for partido in partidos_ordenados:
        if partido.goles_chabas >= partido.goles_rival:
            racha_actual_no_perdidos += 1
            max_racha_no_perdidos = max(max_racha_no_perdidos, racha_actual_no_perdidos)
        else:
            racha_actual_no_perdidos = 0

        if partido.goles_chabas > partido.goles_rival:
            racha_actual_ganados += 1
            max_racha_ganados = max(max_racha_ganados, racha_actual_ganados)
        else:
            racha_actual_ganados = 0

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
        'max_racha_ganados': max_racha_ganados,
    }

    return render(request, 'historial/historicos.html', {
        'partidos': partidos_mostrados,  # Se muestran en la tabla
        'temporadas': temporadas,
        'equipos': equipos,
        'años': [año.year for año in años_disponibles],
        'partidos_disponibles': partidos_disponibles,
        'jugadores': jugadores,
        'filtros': {
            'temporada': temporada_seleccionada,
            'equipo': equipo_seleccionado,
            'anio': año_seleccionado,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'ultimos': ultimos_n,
            'desde_partido': desde_partido_id,
            'jugador': jugador_id,
            'accion': accion,
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
        partidos = Partido.objects.filter(rival=club, jugado=True)

        ganados = partidos.filter(goles_chabas__gt=F('goles_rival')).count()
        empatados = partidos.filter(goles_chabas=F('goles_rival')).count()
        perdidos = partidos.filter(goles_chabas__lt=F('goles_rival')).count()

        data.append({
            'nombre': club.nombre,
            'fundacion': club.fundacion,
            'campeonatos': club.campeonatos,
            'escudo': club.escudo,
            'ganados': ganados,
            'empatados': empatados,
            'perdidos': perdidos,
        })

    return render(request, 'historial/rivales.html', {'clubes': data})

def jugadores_por_anio(request):
    anio = request.GET.get('anio')

    jugadores = Jugador.objects.none()
    anios_disponibles = Torneo.objects.dates('fecha_inicio', 'year', order='DESC')

    if anio:
        torneos_en_anio = Torneo.objects.filter(
            Q(fecha_inicio__year=anio) | Q(fecha_fin__year=anio)
        )
        jugadores = Jugador.objects.filter(
            participacionjugador__torneo__in=torneos_en_anio,
            
        ).distinct()

    context = {
        'anios_disponibles': [a.year for a in anios_disponibles],
        'jugadores': jugadores,
        'anio_seleccionado': anio,
    }

    return render(request, 'historial/jugadores_por_anio.html', context)

def sobre_datos(request):
    return render(request, 'historial/sobre_datos.html')