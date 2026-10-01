from pathlib import Path

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

DOSSIER = Path(__file__).resolve().parent
CHEMIN_IMAGE = DOSSIER / "Images" / "lenaAEgaliser.jpg"

image_bgr = cv.imread(str(CHEMIN_IMAGE), cv.IMREAD_COLOR)
if image_bgr is None:
    raise FileNotFoundError(f"Impossible de charger {CHEMIN_IMAGE}")

image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
canaux_rgb = cv.split(image_rgb)
canaux_rgb_egalises = [cv.equalizeHist(canal) for canal in canaux_rgb]
image_rgb_egalisee = cv.merge(canaux_rgb_egalises)
image_bgr_egalisee_rgb = cv.cvtColor(image_rgb_egalisee, cv.COLOR_RGB2BGR)

ycrcb = cv.cvtColor(image_bgr, cv.COLOR_BGR2YCrCb)
luminance, canal_cr, canal_cb = cv.split(ycrcb)
luminance_egalisee = cv.equalizeHist(luminance)
ycrcb_egalise = cv.merge((luminance_egalisee, canal_cr, canal_cb))
image_bgr_egalisee_luminance = cv.cvtColor(ycrcb_egalise, cv.COLOR_YCrCb2BGR)

image_luminance_rgb = cv.cvtColor(image_bgr_egalisee_luminance, cv.COLOR_BGR2RGB)
fig_images, axes_images = plt.subplots(1, 3, figsize=(14, 5))
for axe, image, titre in zip(
    axes_images,
    (image_rgb, image_rgb_egalisee, image_luminance_rgb),
    ("Originale", "Egalisation des canaux RGB", "Egalisation de la luminance Y"),
):
    axe.imshow(image)
    axe.set_title(titre)
    axe.axis("off")
fig_images.tight_layout()

fig_hist, axes_hist = plt.subplots(1, 3, figsize=(16, 4.5))
for axe, canaux, titre in (
    (axes_hist[0], canaux_rgb, "Histogramme RGB original"),
    (axes_hist[1], canaux_rgb_egalises, "Histogramme après égalisation RGB"),
):
    for canal, couleur, nom in zip(canaux, ("red", "green", "blue"), ("R", "G", "B")):
        histogramme = cv.calcHist([canal], [0], None, [256], [0, 256])
        axe.plot(histogramme, color=couleur, label=nom)
    axe.set_title(titre)
    axe.set_xlabel("Intensité")
    axe.set_ylabel("Nombre de pixels")
    axe.set_xlim(0, 255)
    axe.legend()

hist_luminance = cv.calcHist([luminance], [0], None, [256], [0, 256])
hist_luminance_egalisee = cv.calcHist(
    [luminance_egalisee], [0], None, [256], [0, 256]
)
axes_hist[2].plot(hist_luminance, color="gray", label="Y originale")
axes_hist[2].plot(hist_luminance_egalisee, color="orange", label="Y égalisée")
axes_hist[2].set_title("Histogramme de la luminance Y")
axes_hist[2].set_xlabel("Intensité")
axes_hist[2].set_ylabel("Nombre de pixels")
axes_hist[2].set_xlim(0, 255)
axes_hist[2].legend()
fig_hist.tight_layout()

print("Méthode généralement préférable : égaliser la luminance Y.")
print("Elle améliore le contraste en préservant mieux les couleurs que l'égalisation indépendante des canaux RGB.")

plt.show()
