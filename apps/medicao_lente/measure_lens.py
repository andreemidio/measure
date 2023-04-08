from math import floor
from typing import Tuple

import cv2
import numpy as np
from shapely import LineString, Point
from shapely.geometry import Polygon


class MeasurementLens:

    def __int__(self):
        ...

    def _resize_image(self, image: np.ndarray, size: Tuple[int, int]):
        h, w = image.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC

        # aspect ratio of image
        aspect = w / h  # if on Python 2, you might need to cast as a float: float(w)/h

        # compute scaling and pad sizing
        if aspect > 1:  # horizontal image
            new_w = sw
            new_h = np.round(new_w / aspect).astype(int)
            pad_vert = (sh - new_h) / 2
            _, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            _, pad_right = 0, 0
        elif aspect < 1:  # vertical image
            new_h = sh
            new_w = np.round(new_h * aspect).astype(int)
            pad_horz = (sw - new_w) / 2
            _, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            _, pad_bot = 0, 0
        else:  # square image
            new_h, new_w = sh, sw
            _, pad_right, pad_top, pad_bot = 0, 0, 0, 0

        # scale and pad
        scaled_img = cv2.resize(image, (new_w, new_h), interpolation=interp)

        return scaled_img

    def cart2polar(self, x, y):
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)
        return r, theta

    def _max_value(self, points):
        max_x1, max_x2 = 0, 0
        for contour in points:
            for point in contour:
                x = point[0][0]
                if x > max_x1:
                    max_x2 = max_x1
                    max_x1 = x
                elif x > max_x2:
                    max_x2 = x

        return max_x1, max_x2

    def _rotate_image(self, image: np.ndarray, points) -> np.ndarray:
        resultado_image = image.copy()
        height, width, channels = image.shape

        if height > width:
            part_width = height // 3

            print(points)

            print("Height Ganhou")

            # Slice the image into three parts
            part1 = img[:part_width, :]
            part2 = img[part_width:part_width * 2, :]
            part3 = img[part_width * 2:, :]

            max_value_in_y_axis = np.max(points)

            p = np.vstack([contour.reshape(-1, 2) for contour in points])

            max_x, max_y = np.max(p, axis=0)

            cv2.namedWindow('ksks', cv2.WINDOW_KEEPRATIO)
            cv2.imshow("part1", part1)
            cv2.imshow("part2", part2)
            cv2.imshow("part3", part3)
            cv2.waitKey(0)

        if width > height:
            part_width = width // 3
            print(points)
            print("Width Ganhou")

            # Find the two highest X values

            p = np.vstack([contour.reshape(-1, 2) for contour in points])

            max_x, max_y = np.max(p, axis=0)

            # max_vales = np.ndarray([int(max_x), int(max_y)])
            #
            # max_vales.reshape(-1, 2)

            p1 = Point(max_x, max_y)

            # Slice the image into three parts
            # part1 = img[:, :part_width]
            part1 = int(width / 3)
            part2 = img[:, part_width:part_width * 2]
            part3 = img[:, part_width * 2:]

            # pts_image_1 = part1.reshape(-1, 2)
            # polygon_image_1 = Polygon(pts_image_1)
            pts_image_2 = part1.reshape(-1, 2)
            polygon_image_2 = Polygon(pts_image_2)
            pts_image_3 = part1.reshape(-1, 2)
            polygon_image_3 = Polygon(pts_image_3)

            # resultado_image1 = polygon_image_1.contains(p1)
            resultado_image2 = polygon_image_2.contains(p1)
            resultado_image3 = polygon_image_3.contains(p1)

            cv2.namedWindow('ksks', cv2.WINDOW_KEEPRATIO)
            cv2.imshow("part1", part1)
            cv2.imshow("part2", part2)
            cv2.imshow("part3", part3)
            cv2.waitKey(0)

        return image

    def get_aruco(self, image: np.ndarray) -> Tuple[float, int, int]:

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)

        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)

        perimeter_aruco = cv2.arcLength(markerCorners[0], True)

        minRect = cv2.minAreaRect(markerCorners[0][0])
        scale = 32 / (float(float(minRect[1][0]) + float(minRect[1][1])) / 2)

        # image_result = self._rotate_image(image, markerCorners)

        return scale

    def _cartesian_to_polar(self, x, y, x_c=0, y_c=0, deg=True):
        complex_format = x - (-1 * x_c) + 1j * ((-1 * y) - (-1 * y_c))
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

        # proporcao, altura_aruco_pixel, largura_aruco_pixel, fator = self.get_aruco(image)
        scale = self.get_aruco(image)

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

        (x, y, w, h) = cv2.boundingRect(contours[0])

        c = max(contours, key=cv2.contourArea)
        x1, y1, largura_lente_pixel, altura_lente_pixel = cv2.boundingRect(c)

        largura = x + w
        altura = y + altura_lente_pixel

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)

        box = np.intp(box)

        vvv = box[3][0] - box[0][0]

        # cv2.rectangle(out, (x1, y1), (x1 + largura_lente_pixel, y1 + altura_lente_pixel), (0, 255, 0), 2)

        for i in box:
            cv2.circle(out, (i[0], i[1]), 3, (0, 255, 0), -1)

        list_values_line = list()

        # cv2.line(out, (x1, y1), (sss, hhh), (255, 255, 255), 2)

        imagem_nova = np.zeros(out.shape, dtype=np.uint8)

        sss = int((x1 + largura_lente_pixel) / 2)
        hhh = int((y1 + altura_lente_pixel) / 2)

        cv2.line(imagem_nova, (x1, y1), (x1 + largura_lente_pixel, y1 + altura_lente_pixel), (255, 255, 255), 2)
        cv2.line(imagem_nova, (x1 + largura_lente_pixel, y1), (x1, y1 + altura_lente_pixel), (255, 255, 255), 2)

        contour = contours[0]
        pts = contour.reshape(-1, 2)
        polygon = Polygon(pts)

        line1 = LineString([(x1, y1), (x1 + largura_lente_pixel, y1 + altura_lente_pixel)])
        line2 = LineString([(x1 + largura_lente_pixel, y1), (x1, y1 + altura_lente_pixel)])

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
        N = 360
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
            r, ang = self._cartesian_to_polar(col[0], row[0], x_c=centroid_x, y_c=centroid_y)

            # raios.append(round((r * 5) / 2))
            raios.append(round(radius))

            # Step #6e
            cv2.line(out, (centroid_x, centroid_y), (col[0], row[0]), (0, 255, 0), 1)

        values = dict(
            horizontal=floor(largura_lente_pixel * scale),
            vertical=floor(altura_lente_pixel * scale),
            diagonal=floor(diagonal * scale),
            oma=raios
        )

        return out, values

    def run(self, image: np.ndarray):

        h, w = image.shape[:2]

        if h > 1920 and w > 1080:
            image = self._resize_image(image, (1920, 1080))

        img_bw = image.copy()
        _canny = self._image_processing(image=img_bw)
        contours = self.find_contours(_canny)

        out = image.copy()

        me, values = self.measurement_lens(image=out, img_bw=img_bw, contours=contours)

        return me, values


if __name__ == '__main__':
    # file = r'C:\Users\Sandro Bispo\Desktop\photo_2023-03-22_08-56-00.jpg'
    file = '/home/andre/Desktop/T3Labs/inpecao_lentes/photo_2023-03-31_11-56-54.jpg'
    image = cv2.imread(file)

    measurement = MeasurementLens()

    _, values = measurement.run(image=image)

    print(values)
