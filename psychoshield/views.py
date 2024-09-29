from django.shortcuts import render


# Create your views here.


def index(request):

    return render(request, 'index.html')


def information(request):

    return render(request, 'information.html')


def actividades(request):

    return render(request, 'actividades.html')


def numerosAyuda(request):

    return render(request, 'numerosAyuda.html')


def test(request):

    return render(request, 'test.html')
