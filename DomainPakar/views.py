from django.shortcuts import render, redirect
from DomainPakar.models import Penyakit, Gejala, Pasien
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
import random, string
import sweetify

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

    contexts = {
        'login': userLogin,
    }
    return render(request=request, context=contexts, template_name='diagnosis.html')

def inputPasien(request):
    if request.user.username == 'admin':
        return redirect('/dashboard')
    if request.method == 'POST':
        isibiodata = request.POST.get('BiodataPasien')
        if isibiodata is not None:
            IDPasien = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            namalengkap = request.POST.get('namalengkap')
            tgllahir = request.POST.get('tgllahir')
            jeniskelamin = request.POST.get('jeniskelamin')
            alamat = request.POST.get('alamat')
            nomortelp = request.POST.get('nomortelp')

            pasienObj = Pasien.objects.create(
                IDPasien=IDPasien,
                NamaLengkap=namalengkap,
                TanggalLahir=datetime.strptime(tgllahir, '%Y-%m-%d'),
                JenisKelamin=jeniskelamin,
                Alamat=alamat,
                NomorTelp=nomortelp
            )

            return redirect('/konsultasi')

            # contexts = {
            #     'IdPasien': IDPasien,
            #     'login': False,
            #     'GejalaObj': Gejala.objects.first()
            # }
            # return render(request=request, context=contexts, template_name='pertanyaan.html')

def pertanyaanView(request):
    if request.user.username == 'admin':
        return redirect('/dashboard')
    userLogin = request.user.is_authenticated and request.user.is_superuser
    if request.method == 'POST':
        isiPertanyaan = request.POST.get('TanyaPasien')
        if(isiPertanyaan is not None):
            print(request.POST)
            IDpasien = request.POST.get('IdPasien')
            IDgejala = request.POST.get('IdGejala')

            dump = int(str(IDgejala).replace('G', ''))
            if (dump+1 < 10):
                nextIDGejala = f'G0{dump+1}'
            else:
                nextIDGejala = f'G{dump+1}'


            Iya = True if request.POST.get('Iya') is not None else False
            Tidak = True if request.POST.get('Tidak') is not None else False


            if Iya:
                print("GEJALA IYAAAAAAA")
                gejalaObj = Gejala.objects.get(IDGejala=IDgejala)
                pasienObj = Pasien.objects.get(IDPasien=IDpasien)
                pasienObj.GejalaPasien.add(gejalaObj)
                pasienObj.save()
            elif Tidak:
                # Not Implement yet
                pass

            contexts = {
                'IdPasien': IDpasien,
                'login': userLogin,
                'GejalaObj': Gejala.objects.get(IDGejala=nextIDGejala)
            }

            return render(request=request, context=contexts, template_name='pertanyaan.html')
        else:
            return redirect('/')
    else:
        return redirect('/')