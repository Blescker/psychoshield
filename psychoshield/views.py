from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Test, Question, AnswerOption, PatientResponse, TestResult
from .forms import TestForm
from .forms import LoginForm, RegisterForm  # Importa el formulario
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


@login_required(login_url='/login/')
def index(request):
    if request.user.is_authenticated:
        if request.user.rol == 'psicólogo':

            return redirect('vista_psicologo')
        return render(request, 'index.html')
    else:
        return HttpResponse("Usuario no autenticado")


def information(request):

    return render(request, 'information.html')


def actividades(request):

    return render(request, 'actividades.html')


def numerosAyuda(request):

    return render(request, 'numerosAyuda.html')


def test_psicologico(request):

    # Obtener el test (en este caso, asumimos que solo hay uno, el BDI-2)
    test = Test.objects.get(
        nombre_test="Test Inventario de Depresión de Beck (BDI-2)")

    if request.method == 'POST':
        form = TestForm(request.POST, test_id=test.id)

        if form.is_valid():
            # Procesar los campos adicionales del paciente
            estado_civil = form.cleaned_data['estado_civil']
            edad = form.cleaned_data['edad']
            sexo = form.cleaned_data['sexo']
            ocupacion = form.cleaned_data['ocupacion']
            educacion = form.cleaned_data['educacion']
            psicologo = form.cleaned_data['psicologo']

            # Calcular el resultado total del test
            resultado_total = 0
            for key, value in form.cleaned_data.items():
                if key.startswith('pregunta_'):
                    respuesta = AnswerOption.objects.get(id=value)
                    # Suponiendo que 'valor' es el campo numérico que representa la puntuación
                    resultado_total += respuesta.valor

            # Determinar el nivel de riesgo basado en el resultado total
            nivel_riesgo = calcular_nivel_riesgo(resultado_total)

            # Guardar el resultado del test en la tabla TestResult
            TestResult.objects.create(
                id_usuario=request.user,
                id_test=test,
                resultado_total=resultado_total,
                nivel_riesgo=nivel_riesgo,
                id_psicologo=psicologo
            )

            # Redirigir a una página de resultados o éxito
            return redirect('test_success')

    else:
        form = TestForm(test_id=test.id)

    return render(request, 'test.html', {'form': form, 'test': test})


def calcular_nivel_riesgo(resultado_total):
    if resultado_total <= 13:
        return 'Mínimo'
    elif resultado_total <= 19:
        return 'Leve'
    elif resultado_total <= 28:
        return 'Moderado'
    else:
        return 'Severo'


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso')

                    # Redirige al psicólogo a su vista personalizada
                    if user.rol == 'psicólogo':
                        return redirect('vista_psicologo')
                    else:
                        # Redirige al index si es paciente
                        return redirect('index')
                else:
                    messages.error(request, 'Credenciales incorrectas.')
            except User.DoesNotExist:
                messages.error(request, 'El usuario no existe.')

    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = 'paciente'  # Asignar el rol de 'paciente'
            user.set_password(form.cleaned_data.get(
                'password'))  # Cifrar la contraseña
            user.save()
            messages.success(
                request, 'Registro completado. ¡Puedes iniciar sesión!')
            return redirect('login')

    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def vista_psicologo(request):
    if request.user.rol == 'psicólogo':
        # Obtener los resultados de los tests de los pacientes atendidos por el psicólogo actual
        resultados = TestResult.objects.filter(id_psicologo=request.user)

        return render(request, 'vista_psicologo.html', {'resultados': resultados})
    else:
        return HttpResponse("Acceso denegado: Solo los psicólogos pueden acceder a esta vista.")


@login_required(login_url='/login/')
def agregar_sintomatologia(request, resultado_id):
    # Obtener el resultado del test
    resultado = TestResult.objects.get(id=resultado_id)

    if request.method == 'POST':
        # Guardar la sintomatología presentada
        sintomatologia = request.POST.get('sintomatologia')
        resultado.sintomatologia_presentada = sintomatologia
        resultado.save()
        # Redirige de vuelta a la vista del psicólogo
        return redirect('vista_psicologo')

    return render(request, 'agregar_sintomatologia.html', {'resultado': resultado})


def lista_pacientes(request):
    return render(request, 'lista_pacientes.html')


def resultados_tests(request):
    return render(request, 'resultados_tests.html')


def perfil_psicologo(request):
    return render(request, 'perfil_psicologo.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def test_success(request):
    return render(request, 'test_success.html')
