from FuncSmallplot import *
from utils import *
from Evaluate import *
from Ellipse_Fitting import *


# Params bg:Binary graph(Edge point is 255)
#        k:shrinking scale
#        n:p(in S) is of value “1” if and only if there are at least n pixels within the same grid of value “1”.
def MSKPF(bg,k,n):
    rows = bg.shape[0]
    cols = bg.shape[1]

    #  shrunken image
    sp = getSmallPlot(bg, rows, cols, k, n)
    # Further smoothing of S
    tsp = getSmoothSmaPlt(sp)

    # endpts of tsp
    [left, up, right, down] = findEdgePoint(tsp)
    # fitting points
    fittings = getSmallkk(bg, tsp, k, left, up, right, down)

    fitting_x=[]
    fitting_y=[]
    for p in fittings:
        fitting_x.append(p[0])
        fitting_y.append(p[1])

    # Ellipse fitting
    res = Least_square(fitting_x, fitting_y, len(fitting_x))
    try:
        paras = calEllipse(res)

        print(paras)
    except:
        print('error')




# # test
if __name__=='__main__':
    img=cv2.imread('')
    bg=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    bg=toBinary(bg,200)
    MSKPF(bg,6,2)

