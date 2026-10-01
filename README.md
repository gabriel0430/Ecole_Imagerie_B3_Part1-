# Ecole_Imagerie_B3_Part1-

Ce depot rassemble quatre exercices de traitement d'image avec Python et OpenCV. Les scripts se trouvent dans `Traitement d'image - Bac 3/` et les images sources dans son sous-dossier `Images/`.

## Installation

Python 3 est necessaire. Depuis un terminal, installer les bibliotheques utilisees :

```powershell
python -m pip install opencv-python numpy matplotlib
```

Lancer les commandes depuis le dossier des exercices afin que les chemins relatifs de l'exercice 1 soient resolus :

```powershell
Set-Location -LiteralPath "Traitement d'image - Bac 3"
python .\EXERCICE1.py
python .\Exercice2.py
python .\Exercice3.py
python .\Exercice4.py
```

Les scripts 2 a 4 construisent le chemin de leur image a partir de l'emplacement du script. Les exercices 3 et 4 utilisent Matplotlib pour afficher les figures; fermer la fenetre de figure pour terminer le programme.

## Exercice 1 - Reduction du bruit

**Source :** `Images/paysageBruit.jpg`.

1. Charger l'image couleur avec `cv2.imread`. OpenCV stocke les canaux dans l'ordre BGR.
2. Appliquer un filtre median de taille 5x5. Ce filtre non lineaire est adapte aux pixels impulsionnels noirs et blancs (bruit poivre et sel).
3. Separer les canaux B, G et R. Lisser le canal bleu avec un flou gaussien 5x5; traiter les canaux vert et rouge avec un filtre bilateral (`d=7`, `sigmaColor=75`, `sigmaSpace=75`) pour attenuer le bruit tout en preservant les contours.
4. Recomposer les canaux, puis appliquer `fastNlMeansDenoisingColored` (`h=12`, `hColor=12`, fenetre modele 7, fenetre de recherche 21) pour reduire le bruit residuel.
5. Ajouter des etiquettes, juxtaposer l'original et le resultat, puis reduire l'affichage si sa hauteur depasse 750 pixels.

Le resultat s'affiche dans une fenetre OpenCV et est enregistre sous `paysage_nettoye.jpg` dans le dossier courant.

## Exercice 2 - Separation des poids bleus et des pois rouges

**Source :** `Images/petitsPois.png`.

1. Charger l'image et la convertir de BGR en HSV. La teinte HSV facilite la selection des couleurs sans dependre directement de leur luminosite.
2. Creer le masque bleu avec les bornes HSV `[100, 120, 50]` et `[130, 255, 255]`.
3. Le rouge se trouve aux deux extremites de l'axe de teinte HSV. Il faut reunir les masques `[0, 120, 50]` a `[10, 255, 255]` et `[170, 120, 50]` a `[180, 255, 255]` avec un OU logique (`cv.bitwise_or`).
4. Nettoyer chacun des masques avec une ouverture puis une fermeture morphologique, utilisant un element elliptique 3x3. L'ouverture elimine les petits bruits; la fermeture comble les petites coupures.
5. Afficher les deux masques binaires et l'image d'origine. Le script est prevu pour enregistrer `poids_bleus.png` et `pois_rouges.png` dans le dossier des exercices.

**Attention :** dans l'etat actuel, l'appel `cv.inRange` du premier masque rouge dans `Exercice2.py` ne fournit pas les deux bornes requises. L'execution s'arrete donc avant le nettoyage, l'affichage et l'enregistrement. Cet appel doit recevoir la borne basse `[0, 120, 50]` et la borne haute `[10, 255, 255]`, comme indique ci-dessus.

## Exercice 3 - Egalisation d'histogramme

**Source :** `Images/lenaAEgaliser.jpg`.

Deux traitements sont compares :

1. **Egalisation des canaux RGB :** convertir l'image BGR en RGB, separer R, G et B, appliquer `cv.equalizeHist` independamment a chaque canal, puis recomposer l'image. Cette methode peut modifier les couleurs car chaque canal recoit une transformation differente.
2. **Egalisation de la luminance :** convertir l'image BGR en YCrCb, egaliser seulement le canal Y avec `cv.equalizeHist`, conserver Cr et Cb, puis reconvertir en BGR. Cette methode renforce le contraste tout en preservant mieux les couleurs.

Le script affiche une comparaison de l'image originale et des deux resultats. Une seconde figure trace les histogrammes R, G et B avant et apres l'egalisation independante, ainsi que les histogrammes Y avant et apres l'egalisation de luminance. Les figures sont affichees, mais ne sont pas enregistrees sur disque. Pour cette image, la methode par luminance produit generalement le rendu le plus naturel.

## Exercice 4 - Separation des balanes par taille

**Source :** `Images/balanes.png`.

1. Charger l'image directement en niveaux de gris.
2. Appliquer le seuillage automatique d'Otsu (`THRESH_BINARY + THRESH_OTSU`) pour separer les zones claires du fond sombre. Pour l'image fournie, le seuil detecte est 115.
3. Appliquer une ouverture avec un element elliptique 5x5 pour supprimer les petites taches et separer les objets du bruit.
4. Etiqueter les composantes connexes avec une connectivite de 8 et mesurer l'aire de chaque composante.
5. Classer comme grandes les composantes d'au moins 1000 pixels, comme petites celles d'au moins 30 et de moins de 1000 pixels, et ignorer les composantes plus petites, considerees comme du bruit.
6. Appliquer les masques a l'image en niveaux de gris pour conserver la valeur des pixels des balanes et mettre le fond a zero.

Le script affiche l'originale, les grandes balanes et les petites balanes cote a cote. Il ne cree pas de fichiers de sortie. Sur l'image fournie, le traitement detecte 8 grandes et 38 petites composantes.