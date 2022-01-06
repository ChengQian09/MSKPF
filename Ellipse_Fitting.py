# FUNCTION: fittingByLS-based method
import numpy as np
import math

# function:LS-based method
def Least_square(x,y,n):
    M00 = sum([x[i] ** 4 for i in range(0,n)])
    M01 = sum([(x[i] ** 3) * y[i] for i in range(0, n)])
    M02 = sum([(x[i] ** 2) * (y[i] ** 2) for i in range(0, n)])
    M03 = sum([x[i] ** 3 for i in range(0, n)])
    M04 = sum([(x[i] ** 2) * y[i] for i in range(0, n)])
    M05 = -sum([x[i] ** 2 for i in range(0, n)])

    M10 = sum([(x[i] ** 3) * y[i] for i in range(0, n)])
    M11 = sum([(x[i] ** 2) * (y[i] ** 2) for i in range(0, n)])
    M12 = sum([x[i] * (y[i] ** 3) for i in range(0, n)])
    M13 = sum([(x[i] ** 2) * y[i] for i in range(0, n)])
    M14 = sum([x[i] * (y[i] ** 2) for i in range(0, n)])
    M15 = -sum([x[i] * y[i] for i in range(0, n)])

    M20 = sum([(x[i] ** 2) * (y[i] ** 2) for i in range(0, n)])
    M21 = sum([x[i] * (y[i] ** 3) for i in range(0, n)])
    M22 = sum([y[i] ** 4 for i in range(0,n)])
    M23 = sum([x[i] * (y[i] ** 2) for i in range(0, n)])
    M24 = sum([y[i] ** 3 for i in range(0,n)])
    M25 = -sum([y[i] ** 2 for i in range(0,n)])

    M30 = sum([x[i] ** 3 for i in range(0,n)])
    M31 = sum([(x[i] ** 2) * y[i] for i in range(0, n)])
    M32 = sum([x[i] * (y[i] ** 2) for i in range(0, n)])
    M33 = sum([x[i] ** 2 for i in range(0,n)])
    M34 = sum([x[i] * y[i] for i in range(0,n)])
    M35 = -sum([x[i] for i in range(0,n)])

    M40 = sum([(x[i] ** 2) * y[i] for i in range(0, n)])
    M41 = sum([x[i] * (y[i] ** 2) for i in range(0, n)])
    M42 = sum([y[i] ** 3 for i in range(0,n)])
    M43 = sum([x[i] * y[i] for i in range(0,n)])
    M44 = sum([y[i] ** 2 for i in range(0,n)])
    M45 = -sum([y[i] for i in range(0,n)])

    MM=np.matrix([[M00,M01,M02,M03,M04],
                 [M10,M11,M12,M13,M14],
                 [M20,M21,M22,M23,M24],
                 [M30,M31,M32,M33,M34],
                 [M40,M41,M42,M43,M44]])
    NN=np.matrix([[M05],[M15],[M25],[M35],[M45]])

    paras=np.dot(MM.I,NN)

    return paras

# Calculate ellipse parameters
def calEllipse(paras):
    A=paras[0,0]
    B=paras[1,0]
    C=paras[2,0]
    D=paras[3,0]
    E=paras[4,0]

    Ellipse_paras=[]

    x0=(B*E-2*C*D)/(4*A*C-B*B)
    y0=(B*D-2*A*E)/(4*A*C-B*B)
    a=math.sqrt((2*(A*x0*x0+C*y0*y0+B*x0*y0-1))/(A+C-math.sqrt((A-C)*(A-C)+B*B)))
    b=math.sqrt((2*(A*x0*x0+C*y0*y0+B*x0*y0-1))/(A+C+math.sqrt((A-C)*(A-C)+B*B)))

    if A<C:
        angle=0.5*math.atan(B/(A-C))
    else:
        angle=math.pi/2+0.5*math.atan(B/(A-C))

    if angle>math.pi/2:
        angle=angle-math.pi


    Ellipse_paras.append(x0)
    Ellipse_paras.append(y0)
    Ellipse_paras.append(a)
    Ellipse_paras.append(b)
    Ellipse_paras.append(angle)

    return Ellipse_paras
