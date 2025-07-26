from django import views
from django.conf import settings
from django.conf.urls.static import static
from historial import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('partidos/<int:partido_id>/', views.detalle_partido, name='detalle_partido'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('temporada-actual/', views.temporada_actual, name='temporada_actual'),
    path('historicos/', views.historicos, name='historicos'),
    path('rivales/', views.rivales, name='rivales'),
    path('jugadores_por_anio/', views.jugadores_por_anio, name='jugadores_por_anio'),
    path('sobre_datos/', views.sobre_datos, name='sobre_datos'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ESTO es lo que te falta para servir archivos STATIC
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)