from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Partido, Jugador, Club, Gol, TarjetaAmarilla, TarjetaRoja, Torneo, HitoHistorico
from django.db.models import Count, F, Q, Sum
from django.utils import timezone
import random

def home(request):
    hoy = date.today()
    
    # 1. Partidos principales
    ultimo_partido = Partido.objects.select_related('rival', 'torneo').filter(jugado=True).order_by('-fecha').first()
    proximo_partido = Partido.objects.select_related('rival', 'torneo').filter(jugado=False).order_by('fecha').first()

    # 2. Torneo Actual (El último creado por fecha)
    torneo_actual = Torneo.objects.order_by('-fecha_inicio').first()
    partidos_recientes = []
    top_goleadores = []

    if torneo_actual:
        # Últimos 5 resultados del torneo actual
        partidos_recientes = Partido.objects.filter(torneo=torneo_actual, jugado=True).order_by('-fecha')[:5]
        
        # Top 5 Goleadores del torneo actual
        # Contamos cuántas veces aparece cada jugador en la tabla Gol para este torneo
        top_goleadores = Jugador.objects.filter(gol__partido__torneo=torneo_actual)\
            .annotate(total_goles=Count('gol'))\
            .order_by('-total_goles')[:5]

            # Top 5 Amonestados
        top_5_amonestados = Jugador.objects.filter(tarjetaamarilla__partido__torneo=torneo_actual)\
            .annotate(total_tarjetas=Count('tarjetaamarilla')).order_by('-total_tarjetas')[:5]

    # --- EXPULSADOS ---
        top_5_expulsados = Jugador.objects.filter(tarjetaroja__partido__torneo=torneo_actual)\
            .annotate(total_rojas=Count('tarjetaroja')).order_by('-total_rojas')[:5]
        
        # Obtenemos los últimos 5 partidos ya jugados del torneo actual
        partidos_recientes = Partido.objects.filter(torneo=torneo_actual, jugado=True).order_by('-fecha')[:5]

    # 3. Efemérides y Máxima Goleada
    efemerides = Partido.objects.filter(fecha__day=hoy.day, fecha__month=hoy.month, jugado=True).order_by('-fecha')
    
    maxima_goleada = Partido.objects.filter(goles_chabas__gt=F('goles_rival'))\
        .annotate(dif=F('goles_chabas') - F('goles_rival'))\
        .order_by('-dif').first()

    return render(request, 'historial/home.html', {
        'ultimo_partido': ultimo_partido,
        'proximo_partido': proximo_partido,
        'torneo_actual': torneo_actual,
        'partidos_recientes': partidos_recientes,
        'top_goleadores': top_goleadores,
        'maxima_goleada': maxima_goleada,
        'efemerides': efemerides,
        'top_amonestados': top_5_amonestados,
        'partidos_recientes': partidos_recientes,
        'top_expulsados': top_5_expulsados,
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
        'altura': partido.get_altura_display(),
        'descripcion': partido.descripcion,
        'videos': partido.videos.all()
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

def partidos(request, club_id=None):
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

    if club_id:
        partidos = partidos.filter(rival__id=club_id)
        equipo_seleccionado = str(club_id) 

    elif equipo_seleccionado and equipo_seleccionado.isdigit():
        partidos = partidos.filter(rival__id=int(equipo_seleccionado))

    if temporada_seleccionada:
        partidos = partidos.filter(torneo__nombre=temporada_seleccionada)

    if año_seleccionado and año_seleccionado.isdigit():
        partidos = partidos.filter(fecha__year=int(año_seleccionado))

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

    return render(request, 'historial/partidos.html', {
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

def jugadores_stats(request):
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

    return render(request, 'historial/jugadores_stats.html', {
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
            'id': club.id,
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

def historia_club(request):
    hitos = HitoHistorico.objects.all()
    return render(request, 'historial/historia.html', {
        'hitos': hitos
    })

def historia(request):
    hitos = HitoHistorico.objects.select_related('partido')
    return render(request, 'historia.html', {'hitos': hitos})

def temporadas_stats(request):
    todos_los_torneos = Torneo.objects.all().order_by('-fecha_inicio')
    seleccionados_ids = request.GET.getlist('t')
    
    if not seleccionados_ids:
        torneos_a_procesar = todos_los_torneos
        modo_comparativa = False
    else:
        torneos_a_procesar = Torneo.objects.filter(id__in=seleccionados_ids).order_by('-fecha_inicio')
        modo_comparativa = True

    stats_resultados = []

    for torneo in torneos_a_procesar:
        # 1. Definimos los partidos de ESTE torneo específico dentro del bucle
        partidos_todos = Partido.objects.filter(torneo=torneo, jugado=True).order_by('fecha')
        
        # Partidos de Fase Regular ("Fecha") para puntos
        partidos_fecha = partidos_todos.filter(instancia='Fecha')
        pj_fecha = partidos_fecha.count()
        pg_fecha = partidos_fecha.filter(goles_chabas__gt=F('goles_rival')).count()
        pe_fecha = partidos_fecha.filter(goles_chabas=F('goles_rival')).count()
        
        puntos_obtenidos = (pg_fecha * 3) + pe_fecha
        puntos_posibles = pj_fecha * 3
        porcentaje_puntos = round((puntos_obtenidos / puntos_posibles * 100), 1) if puntos_posibles > 0 else 0

        # 2. Estadísticas Generales del torneo completo
        pj_total = partidos_todos.count()
        gf = partidos_todos.aggregate(Sum('goles_chabas'))['goles_chabas__sum'] or 0
        gc = partidos_todos.aggregate(Sum('goles_rival'))['goles_rival__sum'] or 0
        diff_goles = gf - gc

        # 3. Cálculo de la Racha (Últimos 5 partidos)
        # Traemos los últimos 5 jugados de este torneo
        ultimos_partidos = partidos_todos.order_by('-fecha')[:5]
        racha = []
        for p in reversed(ultimos_partidos): # Invertimos para que el más nuevo esté a la derecha
            if p.goles_chabas > p.goles_rival:
                racha.append('V')
            elif p.goles_chabas < p.goles_rival:
                racha.append('D')
            else:
                racha.append('E')

        # 4. Datos Curiosos Dinámicos
        candidatos = []
        
        # --- Dato: Goleada (La paliza) ---
        gran_victoria = partidos_todos.filter(goles_chabas__gt=F('goles_rival')).order_by('-goles_chabas').first()
        if gran_victoria:
            if gran_victoria.tipo == 'L':
                candidatos.append(f"La locura de local: le metimos un {gran_victoria.goles_chabas}-{gran_victoria.goles_rival} a {gran_victoria.rival.nombre}.")
            else:
                candidatos.append(f"Lo más lindo: el {gran_victoria.goles_chabas}-{gran_victoria.goles_rival} a {gran_victoria.rival.nombre} en su casa.")

        # --- Dato: Valla Invicta (Arco cerrado) ---
        vallas_invictas = partidos_todos.filter(goles_rival=0).count()
        if vallas_invictas > 7:
            candidatos.append(f"En {vallas_invictas} partidos nuestro arco se fue en 0")

        # --- Dato: Tarjetas (Hacha y tiza) ---
        amarillas = TarjetaAmarilla.objects.filter(partido__torneo=torneo).count()
        rojas = TarjetaRoja.objects.filter(partido__torneo=torneo).count()
        if rojas > 3 and amarillas > 10:
            candidatos.append(f"Se jugó con el cuchillo entre los dientes: metimos {amarillas} amarillas y {rojas} rojas.")
        # elif amarillas < 5 and pj_total > 5:
        #    candidatos.append(f"Unos señores: apenas {amarillas} amarillas en todo el torneo. Fair play puro.")

        # --- Dato: Instancia Máxima ---
        # Definimos un orden de importancia para las instancias
        orden_instancias = ['Final', 'FinVue', 'FinIda', 'Semi', 'SemVue', 'SemIda', 'Cua', 'CuaVue', 'CuaIda', 'Oct', 'OctVue', 'OctIda']
        instancia_maxima = "Fase de Grupos"
        
        for inst in orden_instancias:
            if partidos_todos.filter(instancia=inst).exists():
                # Mapeo de nombres para que suene bien
                nombres_bonitos = {
                    'Final': 'la Final', 'FinVue': 'la Final', 'FinIda': 'la Final',
                    'Semi': 'Semis', 'SemVue': 'Semis', 'SemIda': 'Semis',
                    'Cua': 'Cuartos', 'CuaVue': 'Cuartos', 'CuaIda': 'Cuartos'
                }
                instancia_maxima = nombres_bonitos.get(inst, "instancias decisivas")
                break
        
        if instancia_maxima != "Fase de Grupos":
            candidatos.append(f"Nuestra temporada se termino en {instancia_maxima}.")

        # --- Dato: Efectividad (El laburo de la temporada) ---
        if porcentaje_puntos >= 70:
            candidatos.append(f"Campaña de locos. Sacamos el {porcentaje_puntos}% de los puntos.")
        elif porcentaje_puntos <= 35 and pj_total > 0:
            candidatos.append("Torneo para el olvido. A barajar y dar de nuevo.")

       # --- Dato: El Clásico (Contra Huracán) ---
        partidos_clasico = partidos_todos.filter(rival__nombre__icontains='Huracan')
        if partidos_clasico.exists():
            v_c = sum(1 for p in partidos_clasico if p.goles_chabas > p.goles_rival)
            d_c = sum(1 for p in partidos_clasico if p.goles_chabas < p.goles_rival)
            e_c = sum(1 for p in partidos_clasico if p.goles_chabas == p.goles_rival)
            total_c = partidos_clasico.count()

            # Caso 1: Ganamos absolutamente todos
            if v_c == total_c:
                candidatos.append("Paternidad absoluta: este año ganamos todos los clásicos.")
            
            # Caso 2: Invictos (al menos una victoria y empates, pero ninguna derrota)
            elif d_c == 0 and v_c > 0:
                candidatos.append("El pueblo quedó en orden: este año no pudieron festejar ni una vez.")
            
            # Caso 3: Empatamos todos los que jugamos
            elif e_c == total_c:
                candidatos.append("Clásicos trabados: Hubo tablas en todos los enfrentamientos.")
            

        hat_trick = Gol.objects.filter(partido__torneo=torneo)\
            .values('partido', 'jugador__nombre', 'jugador__apellido')\
            .annotate(g=Count('id'))\
            .filter(g__gte=3)\
            .order_by('-g')\
            .first() # Ahora con order_by no tira error
        
        if hat_trick:
            candidatos.append(f"{hat_trick['jugador__nombre']} {hat_trick['jugador__apellido']} clavó tres en un mismo partido y se llevó la pelota.")


        # SELECCIÓN FINAL: Mezclamos para que no sea siempre igual
        if len(candidatos) >= 3:
            datos_curiosos = random.sample(candidatos, 3)
        else:
            datos_curiosos = candidatos

        # 5. Máximo Goleador
        top_g = Jugador.objects.filter(gol__partido__torneo=torneo).annotate(goles_t=Count('gol')).order_by('-goles_t').first()

        stats_resultados.append({
            'torneo': torneo,
            'puntos_obtenidos': puntos_obtenidos,
            'puntos_posibles': puntos_posibles,
            'porcentaje_puntos': porcentaje_puntos,
            'pj': pj_total,
            'gf': gf,
            'gc': gc,
            'diff_goles': diff_goles,
            'racha': racha,
            'goleador': top_g,
            'goles_goleador': top_g.goles_t if top_g else 0,
            'datos_curiosos': datos_curiosos,
        })

    return render(request, 'historial/temporadas_stats.html', {
        'todos_los_torneos': todos_los_torneos,
        'stats': stats_resultados,
        'modo_comparativa': modo_comparativa,
    })