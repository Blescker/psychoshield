from django.urls import path
from psychoshield import views
from django.shortcuts import redirect


urlpatterns = [
    # Redirige la URL raíz al login
    path('', lambda request: redirect('login')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('index/', views.index, name="index"),
    path('information/', views.information, name="information"),
    path('actividades/', views.actividades, name="actividades"),
    path('numerosAyuda/', views.numerosAyuda, name="numerosAyuda"),
    path('test/', views.test_psicologico, name="test"),
    path('logout/', views.logout_view, name="logout"),
    path('test/success/', views.test_success, name='test_success'),

]
