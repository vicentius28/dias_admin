# Generated by Django 4.1.2 on 2023-10-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectoapp', '0004_alter_formulario_jornada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario',
            name='motivo',
            field=models.IntegerField(choices=[[0, 'Dia De Cumpleaños'], [1, 'Dia Administrativo']], default='Dia Administrativo'),
        ),
    ]
