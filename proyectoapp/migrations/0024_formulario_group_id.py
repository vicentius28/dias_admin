# Generated by Django 4.1.2 on 2023-10-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectoapp', '0023_remove_user_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='group_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
