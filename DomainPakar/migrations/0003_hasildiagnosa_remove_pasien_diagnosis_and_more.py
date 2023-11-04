# Generated by Django 4.2.5 on 2023-11-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DomainPakar', '0002_gejalapasien'),
    ]

    operations = [
        migrations.CreateModel(
            name='HasilDiagnosa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDPasien', models.CharField(blank=True, max_length=5, null=True)),
                ('IDPenyakit', models.CharField(blank=True, max_length=4, null=True)),
                ('Persentase', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='pasien',
            name='Diagnosis',
        ),
        migrations.AddField(
            model_name='pasien',
            name='Diagnosis',
            field=models.ManyToManyField(blank=True, to='DomainPakar.hasildiagnosa'),
        ),
    ]