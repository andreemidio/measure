import urllib
import urllib.request

import cv2
import numpy as np
from django.contrib.auth import authenticate
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

        user = Usuarios.objects.get(id="23891265-80e6-44d8-88de-b3573bcf8bfc")

        medicao = {
            'dnp': int(dnp),
            'altura': request.POST.get('altura'),
            'ponte': ponte,
            'OS': request.POST.get('OS'),
            'cnpj_otica': request.POST.get('cnpj_otica'),
            'cnpj_laboratorio': request.POST.get('cnpj_laboratorio'),
            'imagem_lente': request.FILES.get("image"),

            'criado_por': user
        }

        _medicao = DadosMedicao.objects.create(**medicao)

        id_file_url = urllib.request.urlopen(_medicao.imagem_lente.url)
        id_file_cloudnary = np.asarray(bytearray(id_file_url.read()), dtype=np.uint8)
        _image = cv2.imdecode(id_file_cloudnary, cv2.IMREAD_GRAYSCALE)

        lens = mlens.run(image=_image, side=side)

        cv2.imwrite("_image.jpg", _image)

        _image_two = cv2.flip(_image, 1)

        cv2.imwrite("_image_two.jpg", _image_two)

        lens_two = mlens.run(image=_image_two, side=side)

        # if lens_two.get("erro") == 'Aruco not found':
        #     return HttpResponse(lens["erro"])

        if lens.get("erro") == 'Aruco not found':
            return HttpResponse(lens["erro"])

        _medicao.horizontal = lens["values"]["horizontal"]
        _medicao.vertical = lens["values"]["vertical"]
        _medicao.diagonal = lens["values"]["diagonal"]

        s = ''.join(str(x) for x in lens["oma"])
        _medicao.oma = s
        _medicao.processado = True
        _medicao.save()

        return render(request, 'app/obras.html')

    if request.method == "GET":
        # user = Usuarios.objects.get(id="23891265-80e6-44d8-88de-b3573bcf8bfc")
        medicao = DadosMedicao.objects.filter(criado_por_id="23891265-80e6-44d8-88de-b3573bcf8bfc").values()

        contexto = {
            "medicoes": medicao
        }

        return render(request, 'app/obras.html', contexto)


# @login_required
# @autenticacao_necessaria
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
