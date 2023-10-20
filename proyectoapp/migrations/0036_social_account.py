# Generated by Django 4.1.2 on 2023-10-16 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('proyectoapp', '0035_delete_c_re_sociales'),
    ]

    operations = [
        migrations.CreateModel(
            name='social_account',
            fields=[
                ('socialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='socialaccount.socialaccount')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('socialaccount.socialaccount',),
        ),
    ]