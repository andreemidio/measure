import urllib

import cv2
import numpy as np
from celery import shared_task

from apps.medicao_lente.facade import get_image_by_id, update_measure_lens
from apps.medicao_lente.measure_lens import MeasurementLens


class A(object):

    @shared_task()
    def add(self, x, y):
        return x + y


@shared_task
def update_measure_lens_task(id: str, **kwargs):
    update_measure_lens(id=id, **kwargs)


@shared_task
def measure_lens(id: str) -> None:
    measure_lens = MeasurementLens()

    id = get_image_by_id(id=id)

    _id_file_url_image_direito = urllib.request.urlopen(id['imagem_olho_direito'])
    _id_file_cloudnary_image_direito = np.asarray(bytearray(_id_file_url_image_direito.read()), dtype=np.uint8)
    _image_direito = cv2.imdecode(_id_file_cloudnary_image_direito, cv2.IMREAD_GRAYSCALE)

    _mlens_direito = measure_lens.run(image=_image_direito)

    _id_file_url_image_esquerdo = urllib.request.urlopen(id['imagem_olho_esquerdo'])
    _id_file_cloudnary_image_esquerdo = np.asarray(bytearray(_id_file_url_image_esquerdo.read()), dtype=np.uint8)
    _image_esquerdo = cv2.imdecode(_id_file_cloudnary_image_esquerdo, cv2.IMREAD_GRAYSCALE)

    _mlens_esquerdo = measure_lens.run(image=_image_esquerdo)

    data = dict(
        # oma_olho_direito=_mlens_direito['values']['oma'],
        horizontal_olho_direito=_mlens_direito['values']['horizontal'],
        vertical_olho_direito=_mlens_direito['values']['vertical'],
        diagonal_maior_olho_direito=_mlens_direito['values']['diagonal'],
        horizontal_olho_esquerdo=_mlens_esquerdo['values']['horizontal'],
        vertical_olho_esquerdo=_mlens_esquerdo['values']['vertical'],
        diagonal_maior_olho_esquerdo=_mlens_esquerdo['values']['diagonal'],
        processado=True,
        # oma_olho_esquerdo=_mlens_esquerdo['values']['oma'],
    )

    update_measure_lens_task.delay(id=id['id'], **data)

    return True
