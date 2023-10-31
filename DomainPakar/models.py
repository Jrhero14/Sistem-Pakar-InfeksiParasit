from django.db import models

# Create your models here.
class Gejala(models.Model):
    IDGejala = models.CharField(max_length=4, null=True, blank=True)
    NamaGejala = models.CharField(max_length=100, null=True, blank=True)
    Pertanyaan = models.CharField(max_length=255, null=True, blank=True)
    SubPenjelasan = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.id}. {self.NamaGejala}'

class Penyakit(models.Model):
    IDPenyakit = models.CharField(max_length=4, null=True, blank=True)
    NamaPenyakit = models.CharField(max_length=100, null=True, blank=True)
    Definisi = models.TextField(null=True, blank=True)
    Solusi = models.TextField(null=True, blank=True)
    Pencegahan = models.TextField(null=True, blank=True)

    GejalaPenyakit = models.ManyToManyField(Gejala, blank=True)

    def __str__(self):
        return f'{self.id}. {self.NamaPenyakit}'

class Pasien(models.Model):
    IDPasien = models.CharField(max_length=5, null=True, blank=True)
    NamaLengkap = models.CharField(max_length=255)
    TanggalLahir = models.DateField()
    Alamat = models.CharField(max_length=255)
    NomorTelp = models.CharField(max_length=15)

    OPTIONS = [
        ('Laki-Laki', 'Laki-Laki'),
        ('Perempuan', 'Perempuan'),
    ]

    JenisKelamin = models.CharField(max_length=15, choices=OPTIONS, default='Laki-Laki')

    GejalaPasien = models.ManyToManyField(Gejala, blank=True)

    Diagnosis = models.ForeignKey(
        Penyakit,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

    TglDiagnosa = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.id}. {self.NamaLengkap}'
