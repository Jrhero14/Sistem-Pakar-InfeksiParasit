# Generated by Django 4.2.5 on 2023-09-28 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DomainPakar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='Diagnosis',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='DomainPakar.penyakit'),
        ),
    ]