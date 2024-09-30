from django import forms
from .models import User, Question, AnswerOption, PatientResponse


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=191,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo Electrónico',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': True
        })
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': True
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo Electrónico',
                'required': True
            }),
        }

    # Verificación de la confirmación de la contraseña
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class TestForm(forms.Form):
    ESTADO_CIVIL_CHOICES = [
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('viudo', 'Viudo/a'),
        ('separado', 'Separado/a'),
        ('divorciado', 'Divorciado/a'),
    ]

    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('no_decir', 'Prefiero no decirlo'),
    ]

    EDUCACION_CHOICES = [
        ('inicial_completa', 'Inicial completa'),
        ('inicial_incompleta', 'Inicial incompleta'),
        ('primaria_completa', 'Primaria completa'),
        ('primaria_incompleta', 'Primaria incompleta'),
        ('secundaria_completa', 'Secundaria completa'),
        ('secundaria_incompleta', 'Secundaria incompleta'),
        ('tecnica_completa', 'Técnica completa'),
        ('tecnica_incompleta', 'Técnica incompleta'),
        ('universitaria_completa', 'Universitaria completa'),
        ('universitaria_incompleta', 'Universitaria incompleta'),
        ('maestria_completa', 'Maestría completa'),
        ('maestria_incompleta', 'Maestría incompleta'),
        ('doctorado_completo', 'Doctorado completo'),
        ('doctorado_incompleto', 'Doctorado incompleto'),
    ]

    def __init__(self, *args, **kwargs):
        test_id = kwargs.pop('test_id')
        super(TestForm, self).__init__(*args, **kwargs)

        # Agregar los campos adicionales al inicio
        self.fields['estado_civil'] = forms.ChoiceField(
            label='Estado Civil', choices=self.ESTADO_CIVIL_CHOICES, required=True)
        self.fields['edad'] = forms.IntegerField(label='Edad', required=True)
        self.fields['sexo'] = forms.ChoiceField(
            label='Sexo', choices=self.SEXO_CHOICES, required=True)
        self.fields['ocupacion'] = forms.CharField(
            label='Ocupación', max_length=100, required=True)
        self.fields['educacion'] = forms.ChoiceField(
            label='Nivel de Educación', choices=self.EDUCACION_CHOICES, required=True)

        # Obtener los psicólogos para que el usuario elija uno
        self.fields['psicologo'] = forms.ModelChoiceField(
            queryset=User.objects.filter(rol='psicólogo'),
            label='Seleccione su psicólogo',
            required=True
        )

        # Obtener todas las preguntas relacionadas con el test
        preguntas = Question.objects.filter(id_test_id=test_id)

        # Para cada pregunta, crear un campo de selección
        for pregunta in preguntas:
            opciones = AnswerOption.objects.filter(id_pregunta=pregunta)
            opciones_tuple = [(opcion.id, opcion.opcion)
                              for opcion in opciones]

            # Crear un campo de RadioSelect para cada pregunta
            self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                label=pregunta.nombre_pregunta,
                choices=opciones_tuple,
                widget=forms.RadioSelect,
                required=True
            )
