from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        user = self.model(email=self.normalize_email(email), nombre=nombre)
        user.set_password(password)  # Usamos el método que tú has definido
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email, nombre, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    PSICOLOGO = 'psicólogo'
    PACIENTE = 'paciente'
    ROLES = [
        (PSICOLOGO, 'Psicólogo'),
        (PACIENTE, 'Paciente'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=191)
    email = models.EmailField(max_length=191, unique=True)
    # Contraseña cifrada
    contraseña = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Campos adicionales que Django espera
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    # Asignar el gestor de usuarios personalizado
    objects = UserManager()

    # Usamos el email como campo principal para el login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']  # Campos requeridos al crear superusuarios

    def __str__(self):
        return self.email

    # Método para cifrar la contraseña
    def set_password(self, raw_password):
        """Cifra la contraseña y la guarda en el campo contraseña."""
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password):
        """Comprueba si la contraseña ingresada coincide con la cifrada."""
        return check_password(raw_password, self.contraseña)

    # Métodos que Django espera para gestionar permisos y autenticación
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_test = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    ESTADO_CIVIL_CHOICES = [
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('viudo', 'Viudo/a'),
        ('separado', 'Separado/a'),
        ('divorciado', 'Divorciado/a'),
    ]

    estado_civil = models.CharField(
        max_length=10,
        choices=ESTADO_CIVIL_CHOICES,
        default='soltero'
    )

    # Edad
    edad = models.PositiveIntegerField(default=25)

    # Opciones para el sexo
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('no_decir', 'Prefiero no decirlo'),
    ]

    sexo = models.CharField(
        max_length=10,
        choices=SEXO_CHOICES,
        default='no_decir'
    )

    # Ocupación
    ocupacion = models.CharField(max_length=100, default='Desconocida')

    # Opciones para el nivel de educación
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

    educacion = models.CharField(
        max_length=30,
        choices=EDUCACION_CHOICES,
        default='primaria_completa'
    )

    def __str__(self):
        return self.nombre_test


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_pregunta = models.CharField(max_length=191)
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    tipo_respuesta = models.CharField(max_length=50, default='opción múltiple')

    def __str__(self):
        return self.nombre_pregunta


class AnswerOption(models.Model):
    id = models.AutoField(primary_key=True)
    id_pregunta = models.ForeignKey(Question, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=191)
    valor = models.IntegerField()

    def __str__(self):
        return self.opcion


class PatientResponse(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'rol': 'paciente'})
    id_pregunta = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_opcion_respuesta = models.ForeignKey(
        AnswerOption, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Respuesta de {self.id_usuario} a {self.id_pregunta}'


class TestResult(models.Model):
    MINIMO = 'Mínimo'
    LEVE = 'Leve'
    MODERADO = 'Moderado'
    SEVERO = 'Severo'
    NIVELES_RIESGO = [
        (MINIMO, 'Mínimo'),
        (LEVE, 'Leve'),
        (MODERADO, 'Moderado'),
        (SEVERO, 'Severo'),
    ]

    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'rol': 'paciente'})
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    resultado_total = models.IntegerField()
    nivel_riesgo = models.CharField(max_length=20, choices=NIVELES_RIESGO)
    fecha_resultado = models.DateTimeField(auto_now_add=True)
    id_psicologo = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                                     'rol': 'psicólogo'}, related_name='psicologo_resultado')

    def __str__(self):
        return f'Resultado {self.id_test} de {self.id_usuario}'
