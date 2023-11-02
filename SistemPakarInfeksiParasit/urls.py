from django.contrib import admin
from django.urls import path

from DomainPakar import views as PakarViews

urlpatterns = [
    # path('restore/', PakarViews.restore),
    # path('backup/', PakarViews.dumpData),
    path('admin/', admin.site.urls),
    path('login/', PakarViews.loginView),
    path('logout/', PakarViews.logoutView),
    path('penyakit/', PakarViews.penyakitView),
    path('gejala/', PakarViews.gejalaView),
    path('tambahData/', PakarViews.tambahDataPOST),
    path('details/', PakarViews.detailsPenyakitView),
    path('konsultasi/', PakarViews.diagnosisView),
    path('pertanyaan/', PakarViews.pertanyaanView),
    path('inputdataPasien/', PakarViews.inputPasien),
    path('detail-pasien/', PakarViews.detailPasienView),
    path('certain-factor/', PakarViews.rulebase),
    path('dashboard/', PakarViews.indexAdmin),
    path('', PakarViews.indexView),
]
