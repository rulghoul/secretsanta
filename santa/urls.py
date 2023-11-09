"""
URL configuration for santa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from intercambio import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view( template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

    path('', views.inicio, name='home'),
    path("admin/", admin.site.urls),
    path('agregar_santa/', views.SantaCreateView.as_view(), name='agregar_santa'),
    path('update_santa/<int:id_santa>/evento/<int:id_evento>', views.SantaUpdateView, name='update_santa'),
    path('santa/<int:id_santa>/evento/<int:id_evento>/', views.detalle_santa, name='detalle_santa'),
    
    path('eventos/agregar_csv/<int:pk>/', views.agregar_santas_desde_csv, name='importar_santas_csv'),
    path('mis_eventos/', views.mis_eventos, name='mis_eventos'),

    path('eventos/', views.EventoListView.as_view(), name='eventos'),
    path('eventos/agregar/', views.EventoCreateView.as_view(), name='agregar_evento'),
    path('eventos/actualizar/<int:pk>/', views.EventoUpdateView.as_view(), name='actualizar_evento'),
    path('eventos/borrar/<int:pk>/', views.EventoDeleteView.as_view(), name='borrar_evento'),
    path('eventos/detalle/<int:pk>/', views.EventoDetailView.as_view(), name='detalle_evento'),

    path('eventos/realizar_sorteo/<int:evento_id>/', views.realizar_sorteo, name='realizar_sorteo'),
    path('eventos/realizar_nuevo_sorteo/<int:evento_id>/', views.realizar_nuevo_sorteo, name='realizar_nuevo_sorteo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)