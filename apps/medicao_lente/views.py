import urllib
import urllib.request

import cv2
import numpy as np
import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .form import LoginForm
from .decorators import autenticacao_necessaria

from apps.medicao_lente.measure_lens import MeasurementLens
from apps.medicao_lente.models import DadosMedicao

mlens = MeasurementLens()


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# @login_required

@autenticacao_necessaria
def salvar_registro(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if request.POST.get('olho_direito') == "on":
            leituraDireito = True
        else:
            leituraDireito = False

        if request.POST.get('olho_esquerdo') == "on":
            leituraEsquerdo = True
        else:
            leituraEsquerdo = False

        dnp = 0
        if request.POST.get('DNP'):
            dnp = request.POST.get('DNP')

        medicao = {
            'DNP': int(dnp),
            'altura': request.POST.get('altura'),
            'leituraDireito': leituraDireito,
            'leituraEsquerdo': leituraEsquerdo,
            'OS': request.POST.get('OS'),
            'cnpjOtica': request.POST.get('cnpj_otica'),
            'cnpjLaboratorio': request.POST.get('cnpj_laboratorio'),
            'image': request.FILES.get("image")
        }

        _medicao = DadosMedicao.objects.create(**medicao)

        id_file_url = urllib.request.urlopen(_medicao.image.url)
        id_file_cloudnary = np.asarray(bytearray(id_file_url.read()), dtype=np.uint8)
        _image = cv2.imdecode(id_file_cloudnary, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite("test.jpg", _image)

        lens = mlens.run(image=_image)

        _medicao.horizontal = lens["horizontal"]
        _medicao.vertical = lens["vertical"]
        _medicao.diagonalMaior = lens["diagonal_maior"]
        _medicao.save()

        return render(request, 'app/obras.html')

    if request.method == "GET":
        medicao = DadosMedicao.objects.values()

        contexto = {
            "medicoes": medicao
        }

        return render(request, 'app/obras.html', contexto)


# @login_required
@autenticacao_necessaria
def documentacao_1(request):
    medicao = DadosMedicao.objects.all().values()

    contexto = {
        "medicoes": medicao
    }
    return render(request, 'app/documentacao_1.html', contexto)


# @login_required
@autenticacao_necessaria
def documentacao_2(request):
    return render(request, 'app/documentacao_2.html')


# @login_required
@autenticacao_necessaria
def documentacao_3(request):
    return render(request, 'app/documentacao_3.html')


# @login_required
@autenticacao_necessaria
def documentacao_categorias(request):
    return render(request, 'app/documentacao_categorias.html')


# @login_required
@autenticacao_necessaria
def upload(request):
    return render(request, 'app/upload.html')



def autenticar(username, password):
    url = 'http://144.22.211.65/api/restacert/v1/auth/loginweb/'
    data = {
        "password": password,
        "username": username
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=json_data, headers=headers)
    if r.status_code == 200:
        access_token = r.json()['accessToken']
        return access_token
    return None


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            token = autenticar(username, password)
            print(f' O token é :{token}')
            if token is not None:
                request.session['accessToken'] = token
                request.session.set_expiry(14400)
                return redirect('obras')
            else:
                form.add_error(None, 'Username ou password inválidos')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})