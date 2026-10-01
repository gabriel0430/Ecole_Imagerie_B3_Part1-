from pathlib import Path

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

DOSSIER = Path(__file__).resolve().parent
CHEMIN_IMAGE = DOSSIER / "Images" / "balanes.png"

image_gris = cv.imread(str(CHEMIN_IMAGE), cv.IMREAD_GRAYSCALE)
if image_gris is None:
    raise FileNotFoundError(f"Impossible de charger {CHEMIN_IMAGE}")

seuil_otsu, masque_initial = cv.threshold(
    image_gris,
    0,
    255,
    cv.THRESH_BINARY + cv.THRESH_OTSU,
)
noyau = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
masque_nettoye = cv.morphologyEx(masque_initial, cv.MORPH_OPEN, noyau)

nombre_labels, labels, statistiques, _ = cv.connectedComponentsWithStats(
    masque_nettoye,
    connectivity=8,
)
masque_grandes = np.zeros_like(image_gris)
masque_petites = np.zeros_like(image_gris)
seuil_aire_grande = 1000
surface_minimale = 30
nombre_grandes = 0
nombre_petites = 0

for label in range(1, nombre_labels):
    aire = statistiques[label, cv.CC_STAT_AREA]
    if aire >= seuil_aire_grande:
        masque_grandes[labels == label] = 255
        nombre_grandes += 1
    elif aire >= surface_minimale:
        masque_petites[labels == label] = 255
        nombre_petites += 1

image_grandes = cv.bitwise_and(image_gris, image_gris, mask=masque_grandes)
image_petites = cv.bitwise_and(image_gris, image_gris, mask=masque_petites)

print(f"Seuil d'Otsu : {seuil_otsu:.0f}")
print(f"Balanes de grande taille : {nombre_grandes}")
print(f"Balanes de petite taille : {nombre_petites}")

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
for axe, image, titre in zip(
    axes,
    (image_gris, image_grandes, image_petites),
    ("Image originale", "Balanes de grande taille", "Balanes de petite taille"),
):
    axe.imshow(image, cmap="gray", vmin=0, vmax=255)
    axe.set_title(titre)
    axe.axis("off")

fig.tight_layout()
plt.show()
