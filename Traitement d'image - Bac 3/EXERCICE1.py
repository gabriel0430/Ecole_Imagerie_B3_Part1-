import cv2
import numpy as np

# 1. Chargement de l'image
img = cv2.imread('Images/paysageBruit.jpg')

# ---------------------------------------------------------
# ETAPE 1 : Élimination du bruit Poivre & Sel (Non-Linéaire)
# ---------------------------------------------------------
# Le filtre médian est LE filtre de référence pour éliminer 
# complètement les pixels noirs et blancs isolés.
denoised_median = cv2.medianBlur(img, 5)

# ---------------------------------------------------------
# ETAPE 2 : Traitement par canal RGB
# ---------------------------------------------------------
b, g, r = cv2.split(denoised_median)

# Le canal bleu contient le résidu de grain le plus fort :
# On lui applique un lissage gaussien (Linéaire)
b_clean = cv2.GaussianBlur(b, (5, 5), 0)

# Le canal vert garde les détails des palmiers :
# On applique un filtre bilatéral pour lisser en gardant les bords nets
g_clean = cv2.bilateralFilter(g, d=7, sigmaColor=75, sigmaSpace=75)

# Le canal rouge
r_clean = cv2.bilateralFilter(r, d=7, sigmaColor=75, sigmaSpace=75)

# Recomposition RGB
img_rgb = cv2.merge([b_clean, g_clean, r_clean])

# ---------------------------------------------------------
# ETAPE 3 : Débruitage Non-Local Means (Finition globale)
# ---------------------------------------------------------
# Élimine les dernières mouchetures de couleur dans le ciel et l'eau
res_final = cv2.fastNlMeansDenoisingColored(
    img_rgb, 
    None, 
    h=12,               # Force de débruitage luminance
    hColor=12,          # Force de débruitage couleur
    templateWindowSize=7, 
    searchWindowSize=21
)

# ---------------------------------------------------------
# AFFICHAGE CÔTÉ À CÔTÉ
# ---------------------------------------------------------
# Ajout des étiquettes
cv2.putText(img, "Originale (Bruit fort)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(res_final, "Nettoyee", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Fusion horizontale pour comparer
comparaison = cv2.hconcat([img, res_final])

# Redimensionnement pour l'affichage écran
hauteur_max = 750
if comparaison.shape[0] > hauteur_max:
    ratio = hauteur_max / comparaison.shape[0]
    largeur = int(comparaison.shape[1] * ratio)
    comparaison = cv2.resize(comparaison, (largeur, hauteur_max))

cv2.imshow("Resultat Debruitage paysageBruit.jpg", comparaison)
cv2.imwrite("paysage_nettoye.jpg", res_final)
cv2.waitKey(0)
cv2.destroyAllWindows()