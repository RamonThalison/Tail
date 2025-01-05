from PIL import Image
import cv2
import requests
import numpy as np
import matplotlib.pyplot as plt

# Funções auxiliares

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return np.asarray(img)


def img_from_url(url):
    img = Image.open(requests.get(url, stream=True).raw)
    return img

url = 'https://upload.wikimedia.org/wikipedia/en/4/42/Beatles_-_Abbey_Road.jpg'

pil_img = img_from_url(url)
plt.imshow(pil_img)
plt.axis('off')
plt.show()

open_cv_image = convert_from_image_to_cv2(pil_img)
# Convertendo a imagem para escala de cinza (necessário para essa e para as proximas questoes)
gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

# Aplicando o Canny Edge Detector
open_cv_image = cv2.Canny(gray_image, threshold1=100, threshold2=200)

pillow_image = convert_from_cv2_to_image(open_cv_image)
plt.imshow(pillow_image)
plt.axis('off')
plt.show()


# usando a imagem cinza na binarização
_, binarized_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Convertendo a imagem binarizada de volta para o formato PIL para exibição
binarized_pil = convert_from_cv2_to_image(binarized_image)

# Mostrando a imagem binarizada
plt.imshow(binarized_pil)
plt.axis('off')
plt.show()

# Plotando o histograma
plt.figure(figsize=(10, 6))
plt.hist(gray_image.ravel(), bins=256, range=[0, 256], color='black')
plt.title('Histograma de Tons de Cinza')
plt.xlabel('Intensidade de Cinza')
plt.ylabel('Número de Pixels')
plt.show()

# Normalização
imagem_normalizada = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX)

# Equalização
imagem_equalizada = cv2.equalizeHist(imagem_normalizada)

# Mostrando a imagem original, normalizada e equalizada lado a lado
plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.imshow(gray_image, cmap='gray')
plt.title('Imagem em Escala de Cinza')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(imagem_normalizada, cmap='gray')
plt.title('Imagem com Normalização de Histograma')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(imagem_equalizada, cmap='gray')
plt.title('Imagem com Equalização de Histograma')
plt.axis('off')

plt.show()

# Plotando os histogramas das três imagens
plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
plt.hist(gray_image.ravel(), bins=256, range=[0, 256], color='black')
plt.title('Histograma - Escala de Cinza')

plt.subplot(1, 3, 2)
plt.hist(imagem_normalizada.ravel(), bins=256, range=[0, 256], color='black')
plt.title('Histograma - Normalização de Histograma')

plt.subplot(1, 3, 3)
plt.hist(imagem_equalizada.ravel(), bins=256, range=[0, 256], color='black')
plt.title('Histograma - Equalização de Histograma')

plt.show()