from math import atan2, sqrt, pi, sin, cos

import cv2
import numpy as np
from shapely import LineString

from shapely.geometry import Point, Polygon


class MeasurementLens:

    def __int__(self):
        ...

    def _image_processing(self, image: np.ndarray) -> np.ndarray:
        _blur = cv2.GaussianBlur(image, (7, 7), 0)

        _, _threshold = cv2.threshold(_blur, 70, 150, cv2.THRESH_BINARY)

        _canny = cv2.Canny(_blur, 100, 300)

        return _canny

    def find_contours(self, image: np.ndarray):
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return contours

    def read_image(self, filename: str) -> np.ndarray:
        return cv2.imread(filename, 0)

    def measurement_lens(self, image: np.ndarray, img_bw: np.ndarray, contours):
        out = image.copy()

        # Step #4

        conto = max(contours, key=cv2.contourArea)

        ref = np.zeros_like(img_bw)
        cv2.drawContours(ref, contours, 0, 255, 1)

        # Step #5
        M = cv2.moments(contours[0])
        centroid_x = int(M['m10'] / M['m00'])
        centroid_y = int(M['m01'] / M['m00'])

        # Get dimensions of the image
        width = image.shape[1]
        height = image.shape[0]

        (x, y, w, h1) = cv2.boundingRect(contours[0])

        c = max(contours, key=cv2.contourArea)
        x1, y1, w1, h1 = cv2.boundingRect(c)

        # steet = self.getOrientation(c, out)

        largura = x + w
        altura = y + h1

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)

        box = np.intp(box)

        vvv = box[3][0] - box[0][0]

        cv2.rectangle(out, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

        for i in box:
            cv2.circle(out, (i[0], i[1]), 3, (0, 255, 0), -1)

        list_values_line = list()

        dist = cv2.pointPolygonTest(c, (528, 170), False)
        dist1 = cv2.pointPolygonTest(c, (842, 430), False)

        # cv2.line(out, (x1, y1), (sss, hhh), (255, 255, 255), 2)

        imagem_nova = np.zeros(out.shape, dtype=np.uint8)

        sss = int((x1 + w1) / 2)
        hhh = int((y1 + h1) / 2)

        cv2.line(imagem_nova, (x1, y1), (x1 + w1, y1 + h1), (255, 255, 255), 2)
        cv2.line(imagem_nova, (x1 + w1, y1), (x1, y1 + h1), (255, 255, 255), 2)

        contour = contours[0]
        pts = contour.reshape(-1, 2)
        polygon = Polygon(pts)

        line1 = LineString([(x1, y1), (x1 + w1, y1 + h1)])
        line2 = LineString([(x1 + w1, y1), (x1, y1 + h1)])

        resulato1 = line1.intersection(polygon)
        resulato2 = line2.intersection(polygon)

        diagonal: float = float()

        if resulato1.length > resulato2.length:

            diagonal = resulato1.length

            cv2.line(out, (int(resulato1.coords[0][0]), int(resulato1.coords[0][1])),
                     (int(resulato1.coords[1][0]), int(resulato1.coords[1][1])), (255, 255, 255), 2)
        else:

            diagonal = resulato2.length

            cv2.line(out, (int(resulato2.coords[0][0]), int(resulato2.coords[0][1])),
                     (int(resulato2.coords[1][0]), int(resulato2.coords[1][1])), (255, 255, 255), 2)

        # Define total number of angles we want
        N = 800
        raios: list = list()
        # Step #6
        for i in range(N):
            # Step #6a
            tmp = np.zeros_like(img_bw)

            # Step #6b
            theta = i * (360 / N)
            theta *= np.pi / 180.0

            # Step #6c

            largura = int(centroid_x + np.cos(theta) * width)

            altura = int(centroid_y - np.sin(theta) * height)

            cv2.line(tmp, (centroid_x, centroid_y), (largura, altura), 255, 5)

            # Step #6d

            (row, col) = np.nonzero(np.logical_and(tmp, ref))

            radius = np.sqrt(((col[0] / 2.0) ** 2.0) + ((row[0] / 2.0) ** 2.0))

            raios.append(radius)
            polar_image = cv2.linearPolar(tmp, (centroid_x, centroid_y), radius, cv2.WARP_FILL_OUTLIERS)

            # Step #6e
            cv2.line(out, (centroid_x, centroid_y), (col[0], row[0]), (0, 255, 0), 1)

        cmY = ((x1 + w1) * 5) / 34.50
        cmX = ((y1 + h1) * 5) / 34.50
        values = dict(
            horizontal=((x1 + h1) * 5) / 94.9,
            vertical=((y1 + h1) * 4) / 60.9,
            diagonal_maior=(diagonal*61)/498,
            # oma=raios

        )

        return out, values

    def run(self, image: np.ndarray):
        img_bw = image.copy()
        _canny = self._image_processing(image=img_bw)
        contours = self.find_contours(_canny)

        out = image.copy()

        me, values = self.measurement_lens(image=image, img_bw=img_bw, contours=contours)
        return values


if __name__ == '__main__':
    file = r'C:\Users\Sandro Bispo\Desktop\photo_2023-03-22_08-56-00.jpg'
    # file = 'photo_2023-03-22_08-23-22.jpg '
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    measurement = MeasurementLens()

    values = measurement.run(image=image)

    print(values)