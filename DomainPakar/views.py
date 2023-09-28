from django.shortcuts import render, redirect
from DomainPakar.models import Penyakit, Gejala
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def indexView(request):
    userLogin = request.user.is_authenticated and request.user.is_superuser
    contexts = {
        'login': userLogin,
    }
    return render(request=request, context=contexts, template_name='index.html')

def tambahDataPOST(request):
    if request.method == 'POST':
        tambahPenyakit = request.POST.get('TambahPenyakit')
        tambahGejala = request.POST.get('TambahGejala')
        if tambahPenyakit is not None:
            ID = request.POST.get('ID')
            nama = request.POST.get('nama')
            definisi = request.POST.get('definisi')
            solusi = request.POST.get('solusi')
            pencegahan = request.POST.get('pencegahan')

            obj = Penyakit.objects.create(
                IDPenyakit=ID,
                NamaPenyakit=nama,
                Definisi=definisi,
                Solusi=solusi,
                Pencegahan=pencegahan
            )

            # Gejala
            gejalaForms = []
            for i in range(1, 38):
                temp = request.POST.get(f'Gejala{i}')
                if temp is not None:
                    GejalaObj = Gejala.objects.get(IDGejala=temp)
                    obj.GejalaPenyakit.add(GejalaObj)
                else:
                    continue
            obj.save()

            return redirect('/penyakit')

        if tambahGejala is not None:
            ID = request.POST.get('ID')
            nama = request.POST.get('nama')
            pertanyaan = request.POST.get('pertanyaan')
            penjelasan = request.POST.get('penjelasan')
            obj = Gejala.objects.create(
                IDGejala=ID,
                NamaGejala=nama,
                Pertanyaan=pertanyaan,
                SubPenjelasan=penjelasan
            )

            return redirect('/gejala')


def penyakitView(request):
    userLogin = request.user.is_authenticated and request.user.is_superuser
    penyakitObj = Penyakit.objects.all()
    gejalaObj = Gejala.objects.all()
    contexts = {
        'login': userLogin,
        'penyakits': penyakitObj,
        'gejalas': gejalaObj
    }
    return render(request=request, context=contexts, template_name='penyakit.html')

def gejalaView(request):
    userLogin = request.user.is_authenticated and request.user.is_superuser
    gejalatObj = Gejala.objects.all()
    contexts = {
        'login': userLogin,
        'gejalas': gejalatObj
    }
    return render(request=request, context=contexts, template_name='gejala.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    contexts = {}
    return render(request=request, context=contexts, template_name='login.html')

def detailsPenyakitView(request):
    userLogin = request.user.is_authenticated and request.user.is_superuser
    if request.method == 'GET':
        IDPenyakit = request.GET['IdPenyakit']
        if IDPenyakit is not None:
            penyakitObj = Penyakit.objects.get(pk=IDPenyakit)
        else:
            return redirect('/penyakit')
        contexts = {
            'login': userLogin,
            'PenyakitObj': penyakitObj,
            'Gejalas': penyakitObj.GejalaPenyakit.all()
        }
        return render(request=request, context=contexts, template_name='details.html')


def logoutView(request):
    logout(request)
    return redirect('/')
