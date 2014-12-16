"""
Insert Doc Here
"""
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import cv2
import sys


def get_gradient(points, index):
    x = points[:, 0, 0]
    y = points[:, 0, 1]
    for x_loc in range(0, len(x)):
        if x_loc > 2 and x_loc < len(x)-2:
            x_5 = [x[x_loc-2], x[x_loc-1], x[x_loc], x[x_loc+1], x[x_loc+2]]
            y_5 = [y[x_loc-2], y[x_loc-1], y[x_loc], y[x_loc+1], y[x_loc+2]]
            s = interpolate.UnivariateSpline(x_5, y_5)
            xs = np.linspace(x_5[0], x_5[len(x_5)-1])
            ys = s(x_5)
            plt.plot(x_5, ys)
    plt.show()

if __name__ == '__main__':
    print __doc__

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    img = cv2.imread(fn, cv2.CV_LOAD_IMAGE_COLOR)
    imgrey = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    edges = cv2.Canny(imgrey, 500, 500)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)
    length = len(contours)
    if length > 1:
        print 'Too many contours found...'
        for i in range(0, length - 1):
            cv2.drawContours(img, contours, i, (0, (100 / (i + 1)) * length,
                                                (100 / length) * i), 3)
    elif length == 0:
        print 'No contours found in image'
    else:
        cv2.drawContours(img, contours, 0, (0, 255, 0), 2)
        
    cv2.imshow(fn, img)
    cv2.waitKey(0)
