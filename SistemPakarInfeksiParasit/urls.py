from django.contrib import admin
from django.urls import path

from DomainPakar import views as PakarViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', PakarViews.loginView),
    path('logout/', PakarViews.logoutView),
    path('penyakit/', PakarViews.penyakitView),
    path('gejala/', PakarViews.gejalaView),
    path('tambahData/', PakarViews.tambahDataPOST),
    path('details/', PakarViews.detailsPenyakitView),
    path('', PakarViews.indexView),
]
