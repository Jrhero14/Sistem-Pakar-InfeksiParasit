from django.http import HttpResponse
from django.shortcuts import render, redirect
from DomainPakar.models import Gejala, Pasien, CFPakar, Penyakit
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
import random, string
import sweetify
import json

def dumpData(request):
    listGejala = []
    listPenyakit = []

    Gejalas = Gejala.objects.all()
    Penyakits = Penyakit.objects.all()

    for gejala in Gejalas:
        listGejala.append({
            'ID': gejala.IDGejala,
            'NamaGejala': gejala.NamaGejala,
            'Pertanyaan': gejala.Pertanyaan,
            'Penjelasan': gejala.SubPenjelasan
        })

    for penyakit in Penyakits:
        listPenyakit.append({
            'ID': penyakit.IDPenyakit,
            'NamaPenyakit': penyakit.NamaPenyakit,
            'Definisi': penyakit.Definisi,
            'Solusi': penyakit.Solusi,
            'Pencegahan': penyakit.Pencegahan
        })

    # the json file where the output must be stored
    out_file = open("gejala.json", "w")

    json.dump({'gejalas': listGejala}, out_file, indent=6)

    out_file.close()

    out_file = open("penyakit.json", "w")

    json.dump({'penyakit': listPenyakit}, out_file, indent=6)

    out_file.close()

    return redirect('/')

def restore(request):
    # Opening JSON file
    f = open('gejala.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    data = data['gejalas']
    for i in data:
        Gejala.objects.create(
            IDGejala=i['ID'],
            NamaGejala=i['NamaGejala'],
            Pertanyaan=i['Pertanyaan'],
            SubPenjelasan=i['Penjelasan']
        )
        print('GEJALA DIBUAT BERHASIL')

    f.close()
    f = open('penyakit.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    data = data['penyakit']
    for i in data:
        Penyakit.objects.create(
            IDPenyakit=i['ID'],
            NamaPenyakit=i['NamaPenyakit'],
            Definisi=i['Definisi'],
            Solusi=i['Solusi'],
            Pencegahan=i['Pencegahan']
        )
        print('PENYAKIT DIBUAT BERHASIL')
    f.close()

    return redirect('/')

# Create your views here.
def indexView(request):
    if request.user.username == 'admin':
        return redirect('/dashboard')

    userLogin = request.user.is_authenticated and request.user.is_superuser
    contexts = {
        'login': userLogin,
    }
    return render(request=request, context=contexts, template_name='index.html')

def indexAdmin(request):
    userLogin = request.user.is_authenticated and request.user.is_superuser
    pasiens = Pasien.objects.all()
    contexts = {
        'login': userLogin,
        'pasiens': pasiens
    }
    return render(request=request, context=contexts, template_name='admin.html')

def detailPasienView(request):
    IDPasien = request.GET.get('IDPasien')
    userLogin = request.user.is_authenticated and request.user.is_superuser
    if IDPasien is not None:
        pasienObj = Pasien.objects.get(IDPasien=IDPasien)
        contexts = {
            'login': userLogin,
            'Pasien': pasienObj,
            'Gejalas': pasienObj.GejalaPasien.all()
        }
        return render(request=request, context=contexts, template_name='details-pasien.html')

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

            sweetify.success(request, 'Tambah Data Penyakit Berhasil')
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

            sweetify.success(request, 'Tambah Data Gejala Berhasil')
            return redirect('/gejala')

def penyakitView(request):

    if request.method == 'POST':
        if request.POST.get('tambahGejalaKePenyakit') is not None:
            GejalaTambahID = request.POST.get('GejalaTambah')
            IDPenyakit = request.POST.get('IDPenyakit')
            penyakitObj = Penyakit.objects.get(IDPenyakit=IDPenyakit)
            gejalaObj = Gejala.objects.get(IDGejala=GejalaTambahID)
            penyakitObj.GejalaPenyakit.add(gejalaObj)
            penyakitObj.save()

            sweetify.success(request, f'Tambah Gejala {gejalaObj.NamaGejala} ke Penyakit {penyakitObj.NamaPenyakit} Berhasil')
            return redirect('/penyakit')

        if request.POST.get('hapusGejalaDariPenyakit') is not None:
            print(request.POST)
            GejalaID = request.POST.get('GejalaID')
            IDPenyakit = request.POST.get('IDPenyakit')
            penyakitObj = Penyakit.objects.get(IDPenyakit=IDPenyakit)
            gejalaObj = Gejala.objects.get(IDGejala=GejalaID)
            penyakitObj.GejalaPenyakit.remove(gejalaObj)
            print(penyakitObj.GejalaPenyakit.all())
            penyakitObj.save()

            sweetify.success(request,f'Hapus Gejala {gejalaObj.NamaGejala} dari Penyakit {penyakitObj.NamaPenyakit} Berhasil')
            return redirect('/penyakit')

        ID = request.POST.get('ID')
        nama = request.POST.get('nama')
        definisi = request.POST.get('definisi')
        solusi = request.POST.get('solusi')
        pencegahan = request.POST.get('pencegahan')

        obj = Penyakit.objects.get(IDPenyakit=ID)
        obj.NamaPenyakit = nama
        obj.Definisi = definisi
        obj.Solusi = solusi
        obj.Pencegahan = pencegahan
        obj.save()

        sweetify.success(request,f'Perubahan data penyakit berhasil')
        return redirect('/penyakit')


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

    hapusGejalaID = request.GET.get('IDGejalaHapus')
    if hapusGejalaID is not None:
        gejalaObj = Gejala.objects.get(IDGejala=hapusGejalaID)
        gejalaObj.delete()
        sweetify.success(request, 'Hapus Data Gejala Berhasil')
        return redirect('/gejala')

    if request.method == 'POST':
        ID = request.POST.get('ID')
        nama = request.POST.get('nama')
        pertanyaan = request.POST.get('pertanyaan')
        penjelasan = request.POST.get('penjelasan')

        sv = Gejala.objects.get(IDGejala=ID)
        sv.NamaGejala = nama
        sv.Pertanyaan =pertanyaan
        sv.SubPenjelasan = penjelasan
        sv.save()
        sweetify.success(request, 'Perubahan Data Berhasil Disimpan')
        return redirect('/gejala')


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

def diagnosisView(request):
    if request.user.username == 'admin':
        return redirect('/dashboard')
    userLogin = request.user.is_authenticated and request.user.is_superuser

    if request.COOKIES.get('IDPasien') is not None:
        contexts = {
            'login': userLogin,
        }
        return render(request=request, context=contexts, template_name='diagnosis-already.html')

    contexts = {
        'login': userLogin,
    }
    return render(request=request, context=contexts, template_name='diagnosis.html')

def pertanyaanView(request):
    print(request.COOKIES)
    if request.user.username == 'admin':
        return redirect('/dashboard')

    if request.COOKIES.get('IDPasien') is None:
        sweetify.warning(request, 'Maaf Anda belum melakukan pendaftaran Pasien, silakan mendaftar')
        return redirect('/konsultasi')

    userLogin = request.user.is_authenticated and request.user.is_superuser
    if request.method == 'POST':
        isibiodata = request.POST.get('BiodataPasien')
        if isibiodata is not None:
            IDPasien = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            namalengkap = request.POST.get('namalengkap')
            tgllahir = request.POST.get('tgllahir')
            jeniskelamin = request.POST.get('jeniskelamin')
            alamat = request.POST.get('alamat')
            nomortelp = request.POST.get('nomortelp')

            Pasien.objects.create(
                IDPasien=IDPasien,
                NamaLengkap=namalengkap,
                TanggalLahir=datetime.strptime(tgllahir, '%Y-%m-%d'),
                JenisKelamin=jeniskelamin,
                Alamat=alamat,
                NomorTelp=nomortelp
            )
            contexts = {
                'login': userLogin,
            }
            response = render(request=request, context=contexts, template_name='pertanyaan.html')
            response.set_cookie('IDPasien', IDPasien)
            return response
    else:
        contexts = {
            'gejalas': Gejala.objects.all(),
            'login': userLogin,
        }
        response = render(request=request, context=contexts, template_name='pertanyaan.html')
        return response
        # return redirect('/')

def editcf(request):
    if request.method != 'POST':
        return redirect('/certain-factor')

    print(request.POST)
    IDPenyakit = request.POST.get('Penyakit')
    IDGejala = request.POST.get('Gejala')
    MB = float(request.POST.get('MB'))
    MD = float(request.POST.get('MD'))
    CF = MB - MD
    cfobj = CFPakar.objects.get(RelasiPenyakit__IDPenyakit=IDPenyakit, RelasiGejala__IDGejala=IDGejala)
    cfobj.MB = MB
    cfobj.MD = MD
    cfobj.CF = CF
    cfobj.save()

    sweetify.success(request, 'Perubahan nilai CF Berhasil')
    return redirect('/certain-factor')

def rulebase(request):
    hapusCF = request.GET.get('IDCFHapus')
    if hapusCF is not None:
        if CFPakar.objects.filter(pk=hapusCF).exists():
            cfPObj = CFPakar.objects.get(pk=hapusCF)
            cfPObj.delete()
            sweetify.success(request, 'Hapus Nilai CF berhasil')
            return redirect('/certain-factor')

    if request.method == 'POST':
        IDPenyakit = request.POST.get('Penyakit')
        IDGejala = request.POST.get('Gejala')
        MB = float(request.POST.get('MB'))
        MD = float(request.POST.get('MD'))
        CF = MB - MD

        CFPakar.objects.create(
            RelasiPenyakit=Penyakit.objects.get(IDPenyakit=IDPenyakit),
            RelasiGejala=Gejala.objects.get(IDGejala=IDGejala),
            MB=MB,
            MD=MD,
            CF=CF
        )
        sweetify.success(request, 'Tambah Data CF Berhasil')
        return redirect('/certain-factor')

    userLogin = request.user.is_authenticated and request.user.is_superuser
    gejalas = Gejala.objects.all()
    penyakits = Penyakit.objects.all()
    cfpakar = CFPakar.objects.all()
    contexts = {
        'login': userLogin,
        'gejalas': gejalas,
        'penyakits': penyakits,
        'cfpakar': cfpakar
    }
    return render(request=request, context=contexts, template_name='cf.html')