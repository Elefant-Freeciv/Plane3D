import numpy as np

def P2R(radii, angles):
    pi=3.14159
    rect=radii * np.exp(1j*(angles*pi/180))
    x=rect.real
    y=rect.imag
    return [x,y]


def R2P(xy):
    pi=3.14159
    x= xy[0]
    y= xy[1]
    r=np.sqrt(x**2+y**2)
    t=np.arctan2(y,x)*180/pi
    return [r,t]

def rotate2d(x,y,angle):
    polar=R2P((x,y))
    newangle=polar[1]+angle
    X=P2R(polar[0],newangle)
    return [X[0],X[1]]

def rotate3d(x,y,z,xa,ya,za):
    polar=R2P((x,y))
    newangle=polar[1]+za
    X=P2R(polar[0],newangle)
    x=X[0]
    y=X[1]
    polar=R2P((x,z))
    newangle=polar[1]+ya
    X=P2R(polar[0],newangle)
    x=X[0]
    z=X[1]
    polar=R2P((y,z))
    newangle=polar[1]+xa
    X=P2R(polar[0],newangle)
    y=X[0]
    z=X[1]
    return [x,y,z]
