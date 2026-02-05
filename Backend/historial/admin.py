import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from .models import Club, Jugador, ParticipacionJugador, Torneo, Partido, Gol, TarjetaAmarilla, TarjetaRoja, VideoPartido, HitoHistorico

# Configuración global del admin
admin.site.site_header = "Club Atlético Chabás - Administración"
admin.site.index_title = "Panel de Control"

# --- ACCIÓN EXCEL ---
@admin.action(description="Descargar Excel Optimizado (Lectura + Power BI)")
def exportar_partidos_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos_Partidos"

    # Encabezados pensados para análisis de datos
    headers = [
        'ID_Partido', 'Fecha', 'Temporada', 'Rival', 'Condicion', 
        'Instancia', 'Altura', 'Goles_Chabas', 'Goles_Rival', 
        'Diferencia_Goles', 'Resultado', 'Puntos_Obtenidos',
        'Goleadores_Nombres', 'Amonestados', 'Expulsados', 
        'Arbitro', 'Jugado'
    ]
    ws.append(headers)

    # Optimizamos la carga de datos relacionados
    queryset = queryset.select_related('torneo', 'rival').prefetch_related(
        'gol_set__jugador', 'tarjetaamarilla_set__jugador', 'tarjetaroja_set__jugador'
    )

    for p in queryset:
        # 1. Lógica de Resultado y Puntos
        diferencia = p.goles_chabas - p.goles_rival
        if diferencia > 0:
            res_texto, puntos = "Victoria", 3
        elif diferencia < 0:
            res_texto, puntos = "Derrota", 0
        else:
            res_texto, puntos = "Empate", 1

        # 2. Limpieza de Goleadores (Solo nombres para que Power BI agrupe bien)
        nombres_goleadores = ", ".join([g.jugador.apellido for g in p.gol_set.all()])
        
        # 3. Otros datos
        temporada = p.torneo.nombre
        condicion = p.get_tipo_display() # Local o Visitante

        ws.append([
            p.id,
            p.fecha,
            temporada,
            p.rival.nombre,
            condicion,
            p.get_instancia_display(),
            p.get_altura_display(),
            p.goles_chabas,
            p.goles_rival,
            diferencia,
            res_texto,
            puntos,
            nombres_goleadores,
            ", ".join([a.jugador.apellido for a in p.tarjetaamarilla_set.all()]),
            ", ".join([r.jugador.apellido for r in p.tarjetaroja_set.all()]),
            p.arbitro,
            "Sí" if p.jugado else "No"
        ])

    # Ajuste de diseño para el humano que lo lee
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 18

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_club_atletico_chabas.xlsx"'
    wb.save(response)
    return response

# En tu clase PartidoAdmin recordá agregar la acción:
# actions = [exportar_partidos_completo]
# --- ACCIÓN SQL ---
@admin.action(description="Exportar seleccionados a .SQL (INSERTS)")
def exportar_partidos_sql(modeladmin, request, queryset):
    sql_output = "-- Backup de Partidos - Club Atlético Chabás\n"
    table_name = "historial_partido" # Reemplaza 'tuapp' por el nombre real de tu carpeta de app
    
    for p in queryset:
        # Escapamos comillas simples en strings para evitar errores de SQL
        desc = p.descripcion.replace("'", "''") if p.descripcion else ""
        arbitro = p.arbitro.replace("'", "''")
        
        sql_output += (
            f"INSERT INTO {table_name} (fecha, torneo_id, rival_id, arbitro, instancia, tipo, goles_chabas, goles_rival, jugado) "
            f"VALUES ('{p.fecha}', {p.torneo.id}, {p.rival.id}, '{arbitro}', '{p.instancia}', '{p.tipo}', {p.goles_chabas}, {p.goles_rival}, {1 if p.jugado else 0});\n"
        )

    response = HttpResponse(sql_output, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="partidos_backup.sql"'
    return response

# 1. CLUBES
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad', 'fundacion', 'escudo_admin', 'activo')
    list_filter = ('activo', 'localidad')
    search_fields = ('nombre', 'localidad')
    list_editable = ('activo',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'localidad', 'activo')
        }),
        ('Historia', {
            'fields': ('fundacion', 'campeonatos'),
            'classes': ('collapse',)
        }),
        ('Imagen', {
            'fields': ('escudo',),
            'classes': ('collapse',)
        }),
    )

    def escudo_admin(self, obj):
        if obj.escudo:
            return format_html('<img src="{}" width="50" />', obj.escudo.url)
        return "Sin escudo"
    escudo_admin.short_description = 'Escudo'


class ParticipacionJugadorInline(admin.TabularInline):
    model = ParticipacionJugador
    extra = 1

# 2. JUGADORES
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'posicion', 'estado', 'foto_admin', 'torneos_jugados', 
                   'goles_totales', 'amarillas_totales', 'rojas_totales')
    list_filter = ('posicion', 'estado')
    search_fields = ('nombre', 'apellido')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'posicion', 'foto')
        }),
        ('Contrato', {
            'fields': ('estado',),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('goles_totales', 'amarillas_totales', 'rojas_totales'),
            'classes': ('collapse',)
        }),
    )

    inlines = [ParticipacionJugadorInline]

    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Jugador'
    
    def foto_admin(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" />', obj.foto.url)
        return "Sin foto"
    foto_admin.short_description = 'Foto'
    
    def torneos_jugados(self, obj):
        return ", ".join(t.nombre for t in obj.torneos.all())
    torneos_jugados.short_description = 'Torneos Jugados'


# 3. TORNEOS
@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rango_fechas', 'duracion_dias')
    list_filter = ('fecha_inicio',)
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_inicio'
    
    def rango_fechas(self, obj):
        return f"{obj.fecha_inicio} al {obj.fecha_fin}"
    
    def duracion_dias(self, obj):
        return (obj.fecha_fin - obj.fecha_inicio).days
    duracion_dias.short_description = 'Duración (días)'

# 4. ESTADÍSTICAS (Tablas intermedias)
class EstadisticaBaseAdmin(admin.ModelAdmin):
    list_display = ('partido', 'jugador', 'minuto')
    list_select_related = ('partido', 'jugador')
    raw_id_fields = ('jugador',)
    list_filter = ('partido__torneo', 'partido__fecha')

@admin.register(Gol)
class GolAdmin(EstadisticaBaseAdmin):
    pass

@admin.register(TarjetaAmarilla)
class TarjetaAmarillaAdmin(EstadisticaBaseAdmin):
    pass

@admin.register(TarjetaRoja)
class TarjetaRojaAdmin(EstadisticaBaseAdmin):
    pass

# 5. PARTIDOS (con inlines)
class GolInline(admin.TabularInline):
    model = Gol
    extra = 1
    fields = ('jugador', 'minuto')

class AmarillaInline(admin.TabularInline):
    model = TarjetaAmarilla
    extra = 1
    fields = ('jugador', 'minuto')

class RojaInline(admin.TabularInline):
    model = TarjetaRoja
    extra = 1
    fields = ('jugador', 'minuto')

class VideoPartidoInline(admin.TabularInline):
    model = VideoPartido
    extra = 1
    fields = ('url_youtube', 'clasificacion', 'titulo')
    readonly_fields = ('video_preview',)
    def video_preview(self, obj):
         if obj.url_youtube:
             # Esto es solo un ejemplo, necesitarías una forma más robusta de obtener el ID y embeberlo
             youtube_id = obj.get_youtube_id() # Si has implementado este método en el modelo
             if youtube_id:
                    return format_html('<iframe width="200" height="113" src="https://www.youtube.com/embed/{}" frameborder="0" allowfullscreen></iframe>', youtube_id)
             return "No preview"
    video_preview.short_description = "Previsualización"

@admin.register(HitoHistorico)
class HitoHistoricoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'titulo', 'tipo', 'imagen_preview')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'descripcion')
    ordering = ('fecha',)
    autocomplete_fields = ('partido',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="60" />', obj.imagen.url)
        return "Sin imagen"

    imagen_preview.short_description = 'Imagen'

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('fecha','instancia', 'vs_rival', 'jugado','resultado', 'arbitro','altura','torneo_link', 'detalle_link')
    list_filter = ('torneo', 'fecha', 'tipo', 'altura')
    search_fields = ('rival__nombre', 'torneo__nombre', 'arbitro')
    inlines = [GolInline, AmarillaInline, RojaInline, VideoPartidoInline]
    date_hierarchy = 'fecha'

    actions = [exportar_partidos_excel, exportar_partidos_sql] 
    
    fieldsets = (
        (None, {
            'fields': ('fecha', 'torneo', 'rival', 'tipo', 'arbitro', 'instancia', 'altura', 'descripcion', 'jugado')
        }),
        ('Resultado', {
            'fields': ('goles_chabas', 'goles_rival')
        }),
    )

    def vs_rival(self, obj):
        icono = '🏠' if obj.tipo == 'L' else '✈️'
        return f"{icono} vs {obj.rival.nombre}"
    vs_rival.short_description = 'Partido'
    
    def resultado(self, obj):
        return f"{obj.goles_chabas}-{obj.goles_rival}"
    resultado.short_description = 'Resultado'
    
    def torneo_link(self, obj):
        return format_html('<a href="../torneo/{}/">{}</a>', obj.torneo.id, obj.torneo.nombre)
    torneo_link.short_description = 'Torneo'
    
    def detalle_link(self, obj):
        return format_html('<a href="../partido/{}/">📝 Editar</a>', obj.id)
    detalle_link.short_description = 'Acciones'

