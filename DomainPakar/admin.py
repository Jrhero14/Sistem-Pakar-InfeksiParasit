from django.contrib import admin
from DomainPakar.models import Penyakit, Pasien, Gejala
# Register your models here.
admin.site.register(Penyakit)
admin.site.register(Pasien)
admin.site.register(Gejala)