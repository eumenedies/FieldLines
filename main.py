"""
Insert Doc Here
"""
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import cv2
import sys
from numpy.testing import assert_approx_equal
import math

# TODO:
# + Mesh -> equidistant on boundary
# - Boundary Conditions
# - Solve Poisson

# Attempt at using spline interpolation to get gradient at point,
# doesnt work yet #######
# def get_gradient(points, width):
#     x = points[:, 0, 0]
#     y = points[:, 0, 1]
#     for x_loc in range(0, len(x)):
#         if x_loc > 2 and x_loc < len(x)-2:
#             x_5 = [x[x_loc-2], x[x_loc-1], x[x_loc], x[x_loc+1], x[x_loc+2]]
#             y_5 = [y[x_loc-2], y[x_loc-1], y[x_loc], y[x_loc+1], y[x_loc+2]]
#             s = interpolate.UnivariateSpline(x_5, y_5)
#             xs = np.linspace(x_5[0], x_5[len(x_5)-1])
#             ys = s(x_5)
#             plt.plot(x_5, ys)
#     plt.show()


def get_mesh(cnt, width, height):
    max_y = np.max(np.max(cnt, 2), 0)
    x = []
    y = []
    mesh_x = []
    mesh_y = []
    rad = []
    theta = []
    for point in cnt:
        x.append(point[0][0])
        y.append(height - point[0][1])
        rad.append(math.sqrt(math.pow(point[0][0], 2) + math.pow(height - point[0][1], 2)))
        theta.append(math.atan((height - point[0][1])/point[0][0]))
        if np.max(point, 1) == max_y:
            break

    for j in range(0, len(x), len(x)/20):
        plt.axvline(x=x[j])
        mesh_x.append(x[j])
        plt.axhline(y=y[j])
        mesh_y.append(y[j])

    for j in range(cnt[0][0][1], height, (height - cnt[0][0][1])/5):
        mesh_y.append(j)
        plt.axhline(y=j)

    for j in range(x[len(x)-1], width, (width - x[len(x)-1])/5):
        mesh_x.append(j)
        plt.axvline(x=j)

    plt.plot(x, y, "r-")
    plt.ylim([0, height])
    plt.xlim([0, width])
    plt.show()

if __name__ == '__main__':
    print __doc__

    if len(sys.argv) == 2:

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
                                                    (100 / length) * i), 2)
        elif length == 0:
            print 'No contours found in image'
        else:
            cv2.drawContours(img, contours, 0, (0, 255, 0), 2)
            width, height, channels = img.shape
            cnt = contours[0]
            get_mesh(cnt, width, height)

    else:
        print "Usage: main.py filename"