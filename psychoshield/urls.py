from django.urls import path
from psychoshield import views
from django.shortcuts import redirect


urlpatterns = [
    # Redirige la URL raíz al login
    path('', lambda request: redirect('login')),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name="logout"),

    # Rutas generales
    path('index/', views.index, name="index"),
    path('information/', views.information, name="information"),
    path('actividades/', views.actividades, name="actividades"),
    path('numerosAyuda/', views.numerosAyuda, name="numerosAyuda"),

    # Test psicológico
    path('test/', views.test_psicologico, name="test"),
    path('test/success/', views.test_success, name='test_success'),

    # Rutas para psicólogos
    # Vista principal del psicólogo
    path('psicologo/', views.vista_psicologo, name='vista_psicologo'),
    path('psicologo/pacientes/', views.lista_pacientes,
         name='lista_pacientes'),  # Lista de pacientes
    path('psicologo/resultados/', views.resultados_tests,
         name='resultados_tests'),  # Resultados de tests
    path('psicologo/perfil/', views.perfil_psicologo,
         name='perfil_psicologo'),  # Perfil del psicólogo
    path('psicologo/sintomatologia/<int:resultado_id>/',
         views.agregar_sintomatologia, name='agregar_sintomatologia'),

]
