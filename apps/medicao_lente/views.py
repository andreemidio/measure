import urllib
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from django.contrib.auth import authenticate
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.medicao_lente.measure_lens import MeasurementLens
from apps.medicao_lente.models import DadosMedicao
from .decorators import autenticacao_necessaria
from .form import LoginForm
from ..usuarios.models import Usuarios

mlens = MeasurementLens()


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# @autenticacao_necessaria
# @login_required
def salvar_registro(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        side = None
        if request.POST.get('side'):
            side = request.POST.get('side')

        dnp = 0
        if request.POST.get('DNP'):
            dnp = request.POST.get('DNP')

        ponte = 0
        if request.POST.get('ponte'):
            ponte = request.POST.get('ponte')

        user = Usuarios.objects.get(email="andresjc2008@gmail.com")

        os = DadosMedicao.objects.filter(OS=request.POST.get('OS')).exists()

        if os is True:
            return HttpResponse("OS já cadastrada")

        medicao = {
            'dnp': int(dnp),
            'ponte': ponte,
            'OS': request.POST.get('OS'),
            'cnpj_otica': request.POST.get('cnpj_otica'),
            'cnpj_laboratorio': request.POST.get('cnpj_laboratorio'),
            'imagem_lente': request.FILES.get("image"),
            'criado_por': user
        }

        _medicao = DadosMedicao.objects.create(**medicao)

        id_file_url = urllib.request.urlopen(_medicao.imagem_lente.url)
        id_file_cloudnary = np.asarray(
            bytearray(id_file_url.read()), dtype=np.uint8)
        _image = cv2.imdecode(id_file_cloudnary, cv2.IMREAD_GRAYSCALE)
        lens = mlens.run(image=_image, side=side)

        if lens.get("erro") == 'Aruco not found':
            return HttpResponse(lens["erro"])

        _medicao.horizontal = lens["values"]["horizontal"]
        _medicao.vertical = lens["values"]["vertical"]
        _medicao.diagonal = lens["values"]["diagonal"]
        _medicao.oma = lens["oma"]
        _medicao.processado = True

        name = f"OS_{str(_medicao.OS)}_ID_{str(_medicao.id)}.vca"

        os = f'JOB="{_medicao.OS}"'
        hbox = f'HBOX={lens["values"]["horizontal"]};{lens["values"]["horizontal"]}\n'
        vbox = f'HBOX={lens["values"]["horizontal"]};{lens["values"]["horizontal"]}\n'
        fed = f'HBOX={lens["values"]["diagonal"]};{lens["values"]["diagonal"]}\n'

        with open(name, 'w', encoding='utf-8') as file:
            file.write(os)
            file.write(lens["oma"])
            file.write(hbox)
            file.write(vbox)
            file.write(fed)

        path = Path(name)

        with path.open(mode="rb") as f:
            _medicao.oma_file = File(f, name=path.name)
            _medicao.save()

        return render(request, 'app/obras.html')

    if request.method == "GET":
        # user = Usuarios.objects.get(id="23891265-80e6-44d8-88de-b3573bcf8bfc")
        medicao = DadosMedicao.objects.filter().order_by('-data_criacao')

        contexto = {
            "medicoes": medicao
        }

        return render(request, 'app/obras.html', contexto)


# @login_required
# @autenticacao_necessaria
def documentacao_1(request):
    medicao = DadosMedicao.objects.filter(processado=True)

    contexto = {
        "medicoes": medicao,

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                return redirect('obras')
            else:
                form.add_error(None, 'Username ou password inválidos')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
