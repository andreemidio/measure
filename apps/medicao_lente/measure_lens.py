from typing import Tuple

import cv2
import numpy as np
from shapely import LineString
from shapely.geometry import Polygon


class MeasurementLens:

    def __int__(self):
        ...

    def cart2polar(self, x, y):
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return r, theta

    def get_aruco(self, image: np.ndarray) -> Tuple[float, int, int]:

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)

        perimeter_aruco = cv2.arcLength(markerCorners[0], True)

        proporcao_aruco = (perimeter_aruco / (4 * 4))

        (x, y), (width, height), angle = cv2.minAreaRect(markerCorners[0][0])

        x, y, h, w = cv2.boundingRect(markerCorners[0])

        largura_aruco = int((width / proporcao_aruco) * 10)
        altura_aruco = int((height / proporcao_aruco) * 10)

        # cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return proporcao_aruco, altura_aruco, largura_aruco

    def cart_to_pol(self, x, y, x_c=0, y_c=0, deg=True):
        complex_format = x - x_c + 1j * (y - y_c)
        return np.abs(complex_format), np.angle(complex_format, deg=deg)

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

        proporcao, _, _ = self.get_aruco(image)

        out = image.copy()
        # out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        # img_bw = cv2.cvtColor(img_bw, cv2.COLOR_BGR2GRAY)

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
        if resulato1.length < resulato2.length:
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

            radius = np.sqrt(((col[0] - centroid_x) ** 2.0) + ((row[0] - centroid_y) ** 2.0))

            # r, theta = self.cart2polar(col[0], row[0])
            r, theta = self.cart_to_pol(col[0], row[0], x_c=centroid_x, y_c=centroid_y)

            # raios.append(round((r * 5) / 2))
            raios.append(round(radius))

            # Step #6e
            cv2.line(out, (centroid_x, centroid_y), (col[0], row[0]), (0, 255, 0), 1)

        cmY = round(((x1 + w1) * 5) / 34.50)
        cmX = round(((y1 + h1) * 5) / 34.50)

        values = dict(
            horizontal=int((w1 / (proporcao + 10)) * 10),
            vertical=int((h1 / (proporcao + 10)) * 10),
            # horizontal=cmX,
            # veritical=cmY,
            diagonal=int((diagonal / (proporcao + 10)) * 10),
            oma=raios
        )

        return out, values

    def run(self, image: np.ndarray):
        img_bw = image.copy()
        _canny = self._image_processing(image=img_bw)
        contours = self.find_contours(_canny)

        out = image.copy()

        me, values = self.measurement_lens(image=out, img_bw=img_bw, contours=contours)

        return me, values


if __name__ == '__main__':
    # file = r'C:\Users\Sandro Bispo\Desktop\photo_2023-03-22_08-56-00.jpg'
    file = '/home/andre/Desktop/T3Labs/inpecao_lentes/photo_2023-03-10_18-04-04.jpg'
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    measurement = MeasurementLens()

    values = measurement.run(image=image)

    print(values)
