from django.contrib import admin
from DomainPakar.models import Penyakit, Pasien, Gejala, CFPakar, GejalaPasien, HasilDiagnosa
# Register your models here.
admin.site.register(Penyakit)
admin.site.register(Pasien)
admin.site.register(Gejala)
admin.site.register(CFPakar)
admin.site.register(GejalaPasien)
admin.site.register(HasilDiagnosa)