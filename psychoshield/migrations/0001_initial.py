# Generated by Django 5.1.1 on 2024-09-30 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_pregunta', models.CharField(max_length=191)),
                ('tipo_respuesta', models.CharField(default='opción múltiple', max_length=50)),
                ('peso', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_test', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=191)),
                ('email', models.EmailField(max_length=191, unique=True)),
                ('contraseña', models.CharField(max_length=128)),
                ('rol', models.CharField(choices=[('psicólogo', 'Psicólogo'), ('paciente', 'Paciente')], max_length=20)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opcion', models.CharField(max_length=191)),
                ('valor', models.IntegerField()),
                ('id_pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychoshield.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='id_test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychoshield.test'),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resultado_total', models.IntegerField()),
                ('nivel_riesgo', models.CharField(choices=[('Mínimo', 'Mínimo'), ('Leve', 'Leve'), ('Moderado', 'Moderado'), ('Severo', 'Severo')], max_length=20)),
                ('fecha_resultado', models.DateTimeField(auto_now_add=True)),
                ('id_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychoshield.test')),
                ('id_psicologo', models.ForeignKey(limit_choices_to={'rol': 'psicólogo'}, on_delete=django.db.models.deletion.CASCADE, related_name='psicologo_resultado', to='psychoshield.user')),
                ('id_usuario', models.ForeignKey(limit_choices_to={'rol': 'paciente'}, on_delete=django.db.models.deletion.CASCADE, to='psychoshield.user')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='id_creador',
            field=models.ForeignKey(limit_choices_to={'rol': 'psicólogo'}, on_delete=django.db.models.deletion.CASCADE, to='psychoshield.user'),
        ),
        migrations.CreateModel(
            name='PatientResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_respuesta', models.DateTimeField(auto_now_add=True)),
                ('id_opcion_respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychoshield.answeroption')),
                ('id_pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychoshield.question')),
                ('id_usuario', models.ForeignKey(limit_choices_to={'rol': 'paciente'}, on_delete=django.db.models.deletion.CASCADE, to='psychoshield.user')),
            ],
        ),
    ]
