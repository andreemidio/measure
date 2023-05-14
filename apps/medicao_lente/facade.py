from apps.medicao_lente.models import DadosMedicao


def get_image_by_id(id: str) -> str:
    id = DadosMedicao.objects.get(id=id)

    data = dict(
        id=id.id.__str__(),
        imagem_olho_direito=id.imagem_olho_direito.url,
        imagem_olho_esquerdo=id.imagem_olho_esquerdo.url
    )

    return data


def update_measure_lens(id: str, **kwargs) -> None:
    dd = DadosMedicao.objects.filter(id=id)

    dd.update(**kwargs)


if __name__ == '__main__':
    id = get_image_by_id(id="b0b7a49d-bdba-4706-9a8b-093ece3450af")
