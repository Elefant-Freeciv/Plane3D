#texturing
import numpy
from numpy import array
from numpy import matrix as mx
from PIL import Image
from PIL import ImageDraw
from pygame import image as pygameimage

textures={}
print("initialized TEX")

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = mx(matrix, dtype=float)
    B = array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return array(res).reshape(8)

def transformblit(src_tri, dst_tri, src_img, dst_img):
    ((x11,x12), (x21,x22), (x31,x32)) = src_tri
    ((y11,y12), (y21,y22), (y31,y32)) = dst_tri

    M = array([
                     [y11, y12, 1, 0, 0, 0],
                     [y21, y22, 1, 0, 0, 0],
                     [y31, y32, 1, 0, 0, 0],
                     [0, 0, 0, y11, y12, 1],
                     [0, 0, 0, y21, y22, 1],
                     [0, 0, 0, y31, y32, 1]
                ])

    y = array([x11, x21, x31, x12, x22, x32])
    A = numpy.linalg.lstsq(M, y, rcond=None)[0]
    transformed = src_img.transform(dst_img.size, Image.AFFINE, A)
    mask = Image.new('1', dst_img.size)
    maskdraw = ImageDraw.Draw(mask)
    maskdraw.polygon(dst_tri, fill=255)
    dst_img.paste(transformed, mask=mask)
    return dst_img
    
def pilImageToSurface(pilImage):
    return pygameimage.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)

def texture(point1, point2, point3, image, o, dst):
    img = textures[image]
    width=img.width
    height=img.height
    if o == 1:
        srcpoint1 = (width, 0)
        srcpoint2 = (0, 0)
        srcpoint3 = (0, height)
    if o == 2:
        srcpoint1 = (0, 0)
        srcpoint2 = (width, 0)
        srcpoint3 = (width, height)
    if o == 3:
        srcpoint1 = (0, height)
        srcpoint2 = (width, height)
        srcpoint3 = (width, 0)
    if o == 4:
        srcpoint1 = (width, height)
        srcpoint2 = (0, height)
        srcpoint3 = (0,0)
    pilImage = transformblit((srcpoint1, srcpoint2, srcpoint3), (point1, point2, point3), img, dst)
    return pilImage
