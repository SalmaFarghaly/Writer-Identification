
from Preprocessing import *
import cv2
import numpy as np
import math
from imutils.contours import sort_contours
import argparse
import imutils


# Binary=  Noise_Removal(path)
# cropedImage = cropImage(Binary)
# array = getLines(cropedImage)
# print("********************")
# print(array[0].shape)
def remove_small_objects(img, min_size=150):
        # find all your connected components (white blobs in your image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1]
        nb_components = nb_components - 1

        # your answer image
        img2 = img
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] < min_size:
                img2[output == i + 1] = 0

        return img2 

path = "ine19"
img = cv2.imread("outputs\l"+path+".png")
backtorgb = img.copy()
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
# image = remove_small_objects(img.copy())
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# perform edge detection, find contours in the edge map, and sort the
# resulting contours from left-to-right
edged = cv2.Canny(blurred, 30, 150)
contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# print(h[0])
contours = imutils.grab_contours(contours)
contours = sort_contours(contours, method="left-to-right")[0]
backtorgb = cv2.cvtColor(edged.copy(),cv2.COLOR_GRAY2RGB)
# backtorgb = img.copy()
# cv2.imwrite(path, backtorgb)
#         #cv2.imshow('lll', img2)
# cv2.waitKey()
# cv2.destroyAllWindows()
img2 =backtorgb.copy()
# img2 = cv2.cvtColor(img2.copy(),cv2.COLOR_GRAY2RGB)
bounding_rect = np.zeros((len(contours), 6))

for i in range(0, len(contours )):
        
        x, y, w, h = cv2.boundingRect(contours[i])
        if ((w == img2.shape[1]) or (w <= img2.shape[1]+10 and img2.shape[1]-10<=w)) or w*h==1:
            continue 
        cv2.rectangle(img2, (x,y), (x + w, y + h), (0,255,0), 1)
        bounding_rect[i] = (int(x), int(y), int(w), int(h), int(w * h), float(h / w))       
#cv2.drawContours(example_copy, contours, 2, (0, 230, 255), 6)
# Show the image with contours
cv2.imwrite(path+'helloo.png', img2)
cv2.waitKey()
cv2.destroyAllWindows()

bounding_rect = bounding_rect[~np.all(bounding_rect == 0, axis=1)]
 
    #getting aspect ratio
h_to_w_ratio = np.average(bounding_rect[:, 5], axis=0)

    #sort contrours based on top left 
    
bounding_rect_sorted = bounding_rect[bounding_rect[:, 0].argsort()]
print(bounding_rect_sorted)
    #distance between each bounding box - width of the first bounding bx to get the distance between two bounding boxes
diff_dist_word = np.diff(bounding_rect_sorted, axis=0)[:, 0] - bounding_rect_sorted[:-1, 2]
threshold = np.average(np.abs(np.diff(bounding_rect_sorted, axis=0)[:, 0] - bounding_rect_sorted[:-1, 2]))
print(threshold)
print("treshhh")
print(diff_dist_word[np.where(diff_dist_word > threshold)])
    
word_dist = np.average(diff_dist_word[np.where(diff_dist_word > threshold)])
within_word_dist = np.average(np.abs(diff_dist_word[np.where(diff_dist_word < threshold)]))
    #  if line consists of only one word
if math.isnan(word_dist):
    word_dist = 0
if math.isnan(within_word_dist):
    within_word_dist = 0

sdW = np.sqrt(np.var(bounding_rect_sorted[:, 2])) # varies in a specific range
MedianW = np.median(bounding_rect_sorted[:, 2]) # in the middle of all numbers
AverageW = np.average(bounding_rect_sorted[:, 2]) #mean
          
s = str(word_dist)+" " +str(within_word_dist)+" "+ str(sdW)+" " + str(MedianW)+" "+ str(AverageW)+" "+str( h_to_w_ratio)+'\n'
print(s)
f = open("demofile2.txt", "a")
f.write(s)
f.close()
