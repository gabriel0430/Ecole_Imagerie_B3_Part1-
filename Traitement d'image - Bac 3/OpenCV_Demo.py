
#%%Ouverture + affichage image
from tkinter import Tk     #pip install tk
from tkinter.filedialog import askopenfilename
import cv2 as cv #pip install opencv-python
cheminBase= "C:\\Users\\sebad\\Documents\\Images\\"


Tk().withdraw() 
filename = askopenfilename(initialdir = cheminBase)
filename2 = askopenfilename(initialdir = cheminBase)

img = cv.imread(filename)  # BGR
img2 = cv.imread(filename2)
if img is None or img2 is None:
    print("error opening image")
else:
    cv.imshow("First image",img)
    cv.imshow("2nd image",img2)
    cv.waitKey(0)
    cv.destroyAllWindows()





# %%Accéder a un pixel de l'image
from tkinter import Tk     #pip install tk
from tkinter.filedialog import askopenfilename
import cv2 as cv

Tk().withdraw() 
filename = askopenfilename(initialdir = "C:\\Users\\sebad\\Documents\\Images\\")

img = cv.imread(filename)
pixel = img[10,10]
print(pixel)

#%%Récuperer une région d'intérêt dans l'image (ROI - Region Of Interest)
from tkinter import Tk     #pip install tk
from tkinter.filedialog import askopenfilename
import cv2 as cv

Tk().withdraw() 
filename = askopenfilename(initialdir = "C:\\Users\\sebad\\Documents\\Images\\")

img = cv.imread(filename)
roi = img[100:300,50:200]
cv.imshow("ROI",roi)

cv.waitKey(0)
cv.destroyAllWindows()
#%%Récupérer les paramètres d'une image et Ajouter du dessin et du texte
import cv2 as cv
img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\tools.png")
imgOriginale = img.copy()
print(img.shape)
print(img.size)
print(img.dtype)

#Dessiner une ligne (debut, fin, couleur, épaisseur)
cv.line(img,(0,0),(50,50),(0,0,255),3)
#Dessiner un rectangle(coin sup. gauche, coin inférieur droit, couleur, épaisseur)
cv.rectangle(img,(40,150),(85,220),(0,255,0),2)
#Dessiner un cercle(centre, rayon, couleur, épaisseur{-1 pour remplir})
cv.circle(img,(59,85), 15, (255,255,255), -1)
#Dessiner une ellipse
cv.ellipse(img,(145,100),(105,15),72,0,360,(255,255,255),2)
#Ajouter du texte
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,"Ceci est une cle",(15,145), font, .3,(255,255,0),1,cv.LINE_AA)

cv.imshow("Image dessinee",img)
cv.imshow("Image originale",imgOriginale)
cv.waitKey(0)
cv.imwrite("C:\\Users\\sebad\\Documents\\Images\\toolsDessin.png",img)

cv.destroyAllWindows()


#%%Récuper un des canaux de couleurs, fusionner des canaux de couleur
from tkinter import Tk     #pip install tk
from tkinter.filedialog import askopenfilename
import cv2 as cv

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(initialdir = "C:\\Users\\sebad\\Documents\\Images\\")

img = cv.imread(filename,cv.IMREAD_COLOR)
b,g,r = cv.split(img)


if r is None:
    print("error opening image")
else:
    b[:,:]=0
 
    cv.imshow("green",g)
    img = cv.merge((b,g,r))
    cv.imshow("image without blue",img)
    cv.waitKey(0)
    cv.destroyAllWindows()
  
# %%Réaliser un seuillage simple (avec trackbar)
import cv2 as cv
from tkinter import Tk     #pip install tk
from tkinter.filedialog import askopenfilename
import cv2 as cv

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(initialdir = "C:\\Users\\sebad\\Documents\\Images\\")
img = cv.imread(filename,cv.IMREAD_GRAYSCALE)
imgOriginale = img.copy()
def nothing(x):
    print(x)

cv.namedWindow('Seuillage')
cv.createTrackbar('Seuil','Seuillage',0,255,nothing)

thresh = 0
while True:
    cv.imshow('Seuillage',img)

    k = cv.waitKey(1) & 0xFF
    if k == 113: #lettre q
        break
    print("After waitkey")
    newthresh = cv.getTrackbarPos('Seuil','Seuillage')
    if newthresh != thresh:
        thresh = newthresh
        ret,img = cv.threshold(imgOriginale,thresh,255,cv.THRESH_BINARY)
cv.destroyAllWindows()
# %% opérations binaires (AND,OR,NOT,XOR)
import cv2 as cv
import numpy as np


img_tools = cv.imread("C:\\Users\\sebad\\Documents\\Images\\tools.png",cv.IMREAD_GRAYSCALE)
img_mask = img_tools.copy()
ret,img_mask = cv.threshold(img_mask,136,255,cv.THRESH_BINARY)

cv.imshow("Masque",img_mask)
cv.imshow("Image de base",img_tools)

cv.waitKey(0)
img_mask_inverted = cv.bitwise_not(img_mask)
cv.imshow("Masque inversé",img_mask_inverted)

img_tools_and = cv.bitwise_and(img_tools,img_mask)
cv.imshow("AND",img_tools_and)

img_tools_or = cv.bitwise_or(img_tools,img_mask)
cv.imshow("OR",img_tools_or)

img_tools_xor = cv.bitwise_xor(img_tools,img_mask_inverted)
cv.imshow("XOR",img_tools_xor)

cv.waitKey(0)
cv.destroyAllWindows()
# %%Mesure de performances
import cv2 as cv

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\tools.png",cv.IMREAD_GRAYSCALE)
somme=0
iter = 100
for i in range(iter):
    tick_avant = cv.getTickCount()
    #seuillage
    ret,img2 = cv.threshold(img,127,255,cv.THRESH_BINARY)

    tick_apres= cv.getTickCount()

    temps = (tick_apres - tick_avant)/cv.getTickFrequency()

    print(f"Temps pour un seuillage sur une image de {img.shape[0]}*{img.shape[0]}: {temps}secondes")
    somme+=temps
print(f"Temps moyen sur {iter} itérations: {somme/iter}secondes")
# %%Changer d'espace colorimétrique
import cv2 as cv
import numpy as np
flags = [i for i in dir(cv) if i.startswith('COLOR_')]
print( flags )

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\planete.jpg",cv.IMREAD_COLOR)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("SOURCE",img)
cv.imshow("Gray",img_gray)

#Trouver une couleur
green = np.uint8([[[0,0,255 ]]])
hsv_green = cv.cvtColor(green,cv.COLOR_BGR2HSV)
print( hsv_green )

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\petitsPois.png",cv.IMREAD_COLOR)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower_blue = np.array([0,150,00])
upper_blue = np.array([30,255,255])

mask = cv.inRange(img_hsv, lower_blue, upper_blue)
img_bleue = cv.bitwise_and(img,img, mask= mask)

cv.imshow("Originale",img)
cv.imshow("Masque",mask)
cv.imshow("Resultat",img_bleue)

cv.waitKey(0)
cv.destroyAllWindows()


# %%Filtres de convolution

import numpy as np
import cv2 as cv

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\tools.png",cv.IMREAD_GRAYSCALE)
ret,img = cv.threshold(img,127,255,cv.THRESH_BINARY)
#Gradient de sobel
noyau = np.ones((3,3),np.float32)
noyau[0][0]=1/3
noyau[0][1]=0
noyau[0][2]=-1/3
noyau[1][0]=1/3
noyau[1][1]=0
noyau[1][2]=-1/3
noyau[2][0]=1/3
noyau[2][1]=0
noyau[2][2]=-1/3


img_sobel = cv.filter2D(img,-1,noyau)


cv.imshow("Resultat",img_sobel)

noyau=noyau.transpose()
img_sobel2 = cv.filter2D(img,-1,noyau)


cv.imshow("Resultat 2",img_sobel2)
#contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#cv.imshow("findcontours",im2)
cv.waitKey(0)
cv.destroyAllWindows()


# %%Filtres moyenneur, median, gaussien
import numpy as np
import cv2 as cv

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\lenaAEgaliser.jpg",cv.IMREAD_COLOR)
cv.imshow("Lena",img)

img_blur = cv.blur(img,(5,5))
cv.imshow("Blur",img_blur)

img_gaussian_blur = cv.GaussianBlur(img,(9,9),0)
cv.imshow("Gaussian blur",img_gaussian_blur)


img_median_blur = cv.medianBlur(img,5)
cv.imshow("Median blur",img_median_blur)

cv.waitKey(0)
cv.destroyAllWindows()
# %%Erosion,dilatation

import cv2 as cv
import numpy as np


img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\EroDila.png", cv.IMREAD_GRAYSCALE)
cv.imshow("Originale",img)
kernel = np.ones((3,3),np.uint8)

img_erosion = cv.erode(img,kernel,iterations = 1)
cv.imshow("Erosion 1x",img_erosion)

img_erosion2 = cv.erode(img,kernel,iterations = 2)
cv.imshow("Erosion 2x",img_erosion2)


img_dilatee = cv.dilate(img,kernel,iterations = 1)
cv.imshow("Dilatation 1x",img_dilatee)

img_dilatee2 = cv.dilate(img,kernel,iterations = 2)
cv.imshow("Dilatation 2x",img_dilatee2)

cv.waitKey(0)
cv.destroyAllWindows()
# %% Ouverture, fermeture
import cv2 as cv
import numpy as np

img = cv.imread("C:\\Users\\sebad\\Documents\\Images\\EroDila.png", cv.IMREAD_GRAYSCALE)
cv.imshow("Originale",img)
kernel = np.ones((3,3),np.uint8)
img_ouverture = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
cv.imshow("Ouverture",img_ouverture)

kernel = np.ones((3,3),np.uint8)
img_ouverture = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
cv.imshow("Fermeture",img_ouverture)

cv.waitKey(0)
cv.destroyAllWindows()

#%%
