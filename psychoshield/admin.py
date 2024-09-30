from django.contrib import admin
from .models import User, Test, Question, AnswerOption, PatientResponse, TestResult
# Register your models here.

# Clase personalizada para el modelo de usuarios


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rol', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'fecha_registro')

    def save_model(self, request, obj, form, change):
        """
        Sobrescribimos el método save_model para asegurarnos de que las contraseñas se cifran
        correctamente al crear o actualizar un usuario desde el admin.
        """
        if form.cleaned_data.get('contraseña'):  # Verificamos si hay una contraseña
            # Ciframos la contraseña
            obj.set_password(form.cleaned_data['contraseña'])
        super().save_model(request, obj, form, change)  # Guardamos el objeto usuario

# Clase personalizada para el modelo de tests


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('nombre_test', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre_test', 'descripcion')

# Clase personalizada para el modelo de preguntas


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('nombre_pregunta', 'id_test', 'tipo_respuesta')
    search_fields = ('nombre_pregunta',)
    list_filter = ('id_test',)

# Clase personalizada para el modelo de opciones de respuesta


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('id_pregunta', 'opcion', 'valor')
    search_fields = ('opcion',)
    list_filter = ('id_pregunta',)

# Clase personalizada para el modelo de respuestas de pacientes


@admin.register(PatientResponse)
class PatientResponseAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_pregunta',
                    'id_opcion_respuesta', 'fecha_respuesta')
    search_fields = ('id_usuario__nombre', 'id_pregunta__nombre_pregunta')
    list_filter = ('fecha_respuesta', 'id_usuario')

# Clase personalizada para el modelo de resultados


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_test', 'resultado_total',
                    'nivel_riesgo', 'id_psicologo', 'fecha_resultado')
    search_fields = ('id_usuario__nombre',
                     'id_test__nombre_test', 'id_psicologo__nombre')
    list_filter = ('nivel_riesgo', 'fecha_resultado', 'id_psicologo')

# brauliortega@gmail.com 123
