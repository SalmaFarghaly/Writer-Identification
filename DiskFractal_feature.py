import scipy.misc
import numpy as np
import cv2

def fractal_dimension(img, threshold=0.9):
    
    Z = (img*255)/256.0 ##cv2.imread(img , 0)/256.0
    # Only for 2d image
    assert(len(Z.shape) == 2)
    # print("FRACTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    def boxcount(Z, k):
        S = np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                               np.arange(0, Z.shape[1], k), axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k*k))[0])
    
    # Transform Z into a binary array
    Z = (Z < threshold)
    
    # Minimal dimension of image
    p = min(Z.shape)
    
    # Greatest power of 2 less than or equal to p
    n = 2**np.floor(np.log(p)/np.log(2))

    # Extract the exponent
    n = int(np.log(n)/np.log(2))

    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2**np.arange(n, 1, -1)
    

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(boxcount(Z, size))
    
    # Fit the successive log(sizes) with log (counts)
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    # print("WEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    return -1*coeffs[0]



#print("Minkowski–Bouligand dimension (computed): ", fractal_dimension("line.jpeg"))
