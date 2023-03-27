import urllib
import urllib.request

import cv2
import numpy as np
from django.shortcuts import render

from apps.medicao_lente.measure_lens import MeasurementLens
from apps.medicao_lente.models import DadosMedicao

mlens = MeasurementLens()


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# @login_required

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

        dnp = None
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

        medicao = DadosMedicao.objects.create(**medicao)

        id_file_url = urllib.request.urlopen(medicao.image.url)
        id_file_cloudnary = np.asarray(bytearray(id_file_url.read()), dtype=np.uint8)
        _image = cv2.imdecode(id_file_cloudnary, cv2.IMREAD_GRAYSCALE)

        lens = mlens.run(image=_image)

        medicao.horizontal = lens["horizontal"]
        medicao.vertical = lens["vertical"]
        medicao.diagonalMaior = lens["diagonal_maior"]
        medicao.save()

        return render(request, 'app/obras.html')

    if request.method == "GET":
        medicao = DadosMedicao.objects.values()

        contexto = {
            "medicoes": medicao
        }

        return render(request, 'app/obras.html', contexto)


# @login_required
def documentacao_1(request):
    medicao = DadosMedicao.objects.all().values()

    contexto = {
        "medicoes": medicao
    }
    return render(request, 'app/documentacao_1.html', contexto)


# @login_required

def documentacao_2(request):
    return render(request, 'app/documentacao_2.html')


# @login_required
def documentacao_3(request):
    return render(request, 'app/documentacao_3.html')


# @login_required
def documentacao_categorias(request):
    return render(request, 'app/documentacao_categorias.html')


# @login_required
def upload(request):
    return render(request, 'app/upload.html')
