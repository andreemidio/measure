import pprint

import requests
from django.shortcuts import render

from apps.medicao_lente.models import DadosMedicao


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# @login_required

def salvar_registro(request):
    # api = "https://medidor-lentes.herokuapp.com/swagger/lentes/medicao/"
    #
    # if request.method == "POST":
    #     data = json.loads(request.POST)
    #     image = request.FILES.get('image')
    #     DNP = request.POST.get('DNP')
    #     altura = request.POST.get('altura')
    #     # ponte = request.POST.get('ponte')
    #     olho_direito = request.POST.get('olho_direito')
    #     olho_esquerdo = request.POST.get('olho_esquerdo')
    #     OS = request.POST.get('OS')
    #     cnpj_otica = request.POST.get('cnpj_otica')
    #     cnpj_laboratorio = request.POST.get('cnpj_laboratorio')
    #
    #     medicao = {
    #         'DNP': DNP,
    #         'altura': altura,
    #         'olho_direito': olho_direito,
    #         'olho_esquerdo': olho_esquerdo,
    #         'OS': OS,
    #         'cnpj_otica': cnpj_otica,
    #         'cnpj_laboratorio': cnpj_laboratorio,
    #     }
    #
    #     files = {'image': (image.name, image.read(), image.content_type)}
    #
    #     r = requests.post(api, data=medicao, auth=HTTPBasicAuth('administrador', '123456'), files=files)
    #
    #     return render(request, 'app/obras.html')

    if request.method == "GET":
        # requisicao = requests.get(api)
        #
        # try:
        #     lista = requisicao.json()
        # except ValueError:
        #     print("A resposta não chegou com o formato esperado.")
        #
        # dicionario = {}
        # for indice, valor in enumerate(lista):
        #     dicionario[indice] = valor

        contexto = {
            "medicoes": {"ddi":"dd"}
        }

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(contexto)

        return render(request, 'app/obras.html', contexto)


# @login_required
def documentacao_1(request):
    api = "https://medidor-lentes.herokuapp.com/swagger/lentes/medicao/"
    # requisicao = requests.get(api)
    # print(requisicao)

    # try:
    #     lista = requisicao.json()
    # except ValueError:
    #     print("A resposta não chegou com o formato esperado.")

    # dicionario = {}
    # for indice, valor in enumerate(lista):
    #     dicionario[indice] = valor

    medicao = DadosMedicao.objects.all().values()

    dicionario = dict(
        oi="eu sou o goku"
    )
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
