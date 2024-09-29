from django.urls import path
from psychoshield import views


urlpatterns = [
    path('', views.index, name="index"),
    path('information/', views.information, name="information"),
    path('actividades/', views.actividades, name="actividades"),
    path('numerosAyuda/', views.numerosAyuda, name="numerosAyuda"),
    path('test/', views.test, name="test"),
]
