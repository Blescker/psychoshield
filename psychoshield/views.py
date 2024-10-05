from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Test, Question, AnswerOption, PatientResponse, TestResult
from .forms import TestForm
from .forms import LoginForm, RegisterForm  # Importa el formulario
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EditarPerfilForm

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
def vista_psicologo(request, id=None):
    if id:
        # Si se selecciona un paciente específico, obtenemos sus resultados
        paciente = User.objects.get(id=id, rol='paciente')
        resultados = TestResult.objects.filter(id_usuario=paciente)
    else:
        # Obtener los resultados de los pacientes atendidos por el psicólogo
        resultados = TestResult.objects.filter(id_psicologo=request.user)

    return render(request, 'vista_psicologo.html', {'resultados': resultados})


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


@login_required(login_url='/login/')
def lista_pacientes(request):
    query = request.GET.get('q', '')  # Obtener el valor de búsqueda del query
    pacientes = User.objects.filter(rol='paciente')  # Filtrar solo pacientes

    if query:
        # Filtrar pacientes por nombre que coincidan con la búsqueda
        pacientes = pacientes.filter(nombre__icontains=query)

    return render(request, 'lista_pacientes.html', {'pacientes': pacientes, 'query': query})

@login_required(login_url='/login/')
def resultados_tests(request):
    # Obtener todos los resultados de los tests
    resultados = TestResult.objects.all()

    # Filtrar por nivel de riesgo, si es necesario
    filtro_riesgo = request.GET.get('riesgo', '')
    if filtro_riesgo:
        resultados = resultados.filter(nivel_riesgo=filtro_riesgo)

    # Contar los niveles de riesgo
    conteo_riesgos = {
        'Mínimo': TestResult.objects.filter(nivel_riesgo='Mínimo').count(),
        'Leve': TestResult.objects.filter(nivel_riesgo='Leve').count(),
        'Moderado': TestResult.objects.filter(nivel_riesgo='Moderado').count(),
        'Severo': TestResult.objects.filter(nivel_riesgo='Severo').count(),
    }

    return render(request, 'resultados_tests.html', {
        'resultados': resultados,
        'conteo_riesgos': conteo_riesgos,
        'filtro_riesgo': filtro_riesgo,
    })

def perfil_psicologo(request):
    psicologo = request.user
    num_pacientes_atendidos = TestResult.objects.filter(id_psicologo=psicologo).values('id_usuario').distinct().count()

    return render(request, 'perfil_psicologo.html', {
        'psicologo': psicologo,
        'num_pacientes_atendidos': num_pacientes_atendidos
    })

def editar_perfil_psicologo(request):
    psicologo = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=psicologo)
        if form.is_valid():
            form.save()
            return redirect('perfil_psicologo')
    else:
        form = EditarPerfilForm(instance=psicologo)

    return render(request, 'editar_perfil_psicologo.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def test_success(request):
    return render(request, 'test_success.html')

@login_required(login_url='/login/')
def vista_psicologo_detalle(request, id):
    # Obtener el paciente específico
    paciente = User.objects.get(id=id, rol='paciente')
    
    # Obtener los resultados de las pruebas del paciente
    resultados = TestResult.objects.filter(id_usuario=paciente)
    
    return render(request, 'vista_psicologo_detalle.html', {'paciente': paciente, 'resultados': resultados})