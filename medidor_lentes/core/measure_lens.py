import cv2
import numpy as np


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

            raios.append(f"R={round((radius) * 5, 5)}")
            polar_image = cv2.linearPolar(tmp, (centroid_x, centroid_y), radius, cv2.WARP_FILL_OUTLIERS)

            # Step #6e
            cv2.line(out, (centroid_x, centroid_y), (col[0], row[0]), (0, 255, 0), 1)
        cmY = (h * 5) / 34.50
        cmX = (w * 5) / 34.50
        values = dict(
            horizontal=cmX,
            vertical=cmY,
            # oma=raios

        )

        return out, values

    def run(self, image: np.ndarray):
        img_bw = image.copy()
        _canny = self._image_processing(image=img_bw)
        contours = self.find_contours(_canny)

        out = image.copy()

        me, values = self.measurement_lens(image=out, img_bw=img_bw, contours=contours)
        return values


if __name__ == '__main__':
    file = r'C:\Users\Sandro Bispo\Desktop\Imagem_dispositivo.jpg'
    img = cv2.imread(file,cv2.IMREAD_GRAYSCALE)

    measurement = MeasurementLens()

    values = measurement.run(image=img)

    print(values)