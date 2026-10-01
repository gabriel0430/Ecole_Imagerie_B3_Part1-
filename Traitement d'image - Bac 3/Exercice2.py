from pathlib import Path

import cv2 as cv
import numpy as np

DOSSIER = Path(__file__).resolve().parent
CHEMIN_IMAGE = DOSSIER / "Images" / "petitsPois.png"

image = cv.imread(str(CHEMIN_IMAGE), cv.IMREAD_COLOR)
if image is None:
    raise FileNotFoundError(f"Impossible de charger {CHEMIN_IMAGE}")

image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

masque_poids_bleus = cv.inRange(
    image_hsv,
    np.array([100, 120, 50], dtype=np.uint8),
    np.array([130, 255, 255], dtype=np.uint8),
)
masque_pois_rouges = cv.bitwise_or(
    cv.inRange(
        image_hsv,
        
        np.array([10, 255, 255], dtype=np.uint8),
    ),
    cv.inRange(
        image_hsv,
        np.array([170, 120, 50], dtype=np.uint8),
        np.array([180, 255, 255], dtype=np.uint8),
    ),
)

noyau = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
masque_poids_bleus = cv.morphologyEx(masque_poids_bleus, cv.MORPH_OPEN, noyau)
masque_poids_bleus = cv.morphologyEx(masque_poids_bleus, cv.MORPH_CLOSE, noyau)
masque_pois_rouges = cv.morphologyEx(masque_pois_rouges, cv.MORPH_OPEN, noyau)
masque_pois_rouges = cv.morphologyEx(masque_pois_rouges, cv.MORPH_CLOSE, noyau)

chemin_poids_bleus = DOSSIER / "poids_bleus.png"
chemin_pois_rouges = DOSSIER / "pois_rouges.png"
if not cv.imwrite(str(chemin_poids_bleus), masque_poids_bleus):
    raise OSError(f"Impossible d'enregistrer {chemin_poids_bleus}")
if not cv.imwrite(str(chemin_pois_rouges), masque_pois_rouges):
    raise OSError(f"Impossible d'enregistrer {chemin_pois_rouges}")

cv.imshow("Poids bleus - masque binaire", masque_poids_bleus)
cv.imshow("Pois rouges - masque binaire", masque_pois_rouges)
cv.imshow("Image originale", image)
cv.waitKey(0)
cv.destroyAllWindows()
