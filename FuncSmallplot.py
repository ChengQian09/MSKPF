# FUNCTION: MSKPF method function
import cv2
import numpy as np
from queue import Queue
from utils import *

# funciton: Binarization
def toBinary(img,thread):
    rows=img.shape[0]
    cols=img.shape[1]

    for i in range(0,rows):
        for j in range(0,cols):
            if img[i,j]>=thread:
                img[i,j]=255
            else:
                img[i,j]=0

    return img

# function: Calculate the degree of the grid
def degreeSmallplot(img,a,b,k,thread):
    degree=0

    for i in range(0,k):
        for j in range(0,k):
            tx=a+i
            ty=b+j

            if img[tx,ty]==255:
                degree=degree+1

    if degree>=thread:
        return True
    else:
        return False

# function:Reduce the original image by k times to get a small image
def getSmallPlot(bg,rows,cols,k,thread):
    sprows = rows // k + 1
    spcols = cols // k + 1
    sp = np.zeros((sprows, spcols))

    for i in range(0, rows, k):
        for j in range(0, cols, k):
            if i + k < rows and j + k < cols and degreeSmallplot(bg, i, j, k,thread) is True:
                sp[i // k, j // k] = 255
            else:
                sp[i // k, j // k] = 0

    return sp

# function: BFS all arcs in the graph
def getArcs(img):
    rows=img.shape[0]
    cols=img.shape[1]

    visited=np.zeros((rows,cols))
    arcs=[]
    q=Queue(maxsize=0)

    for i in range(0,rows):
        for j in range(0,cols):
            if img[i][j]==255 and visited[i][j]==0:
                arc=[]
                q.put([i,j])
                visited[i][j]=1
                arc.append([i,j])

                while(not q.empty()):
                    tmp=q.get()
                    tx=tmp[0]
                    ty=tmp[1]
                    # (tx-1,ty-1)
                    if tx-1>=0 and ty-1>=0 and img[tx-1][ty-1]==255 and visited[tx-1][ty-1]==0:
                        visited[tx-1][ty-1]=1
                        q.put([tx-1,ty-1])
                        arc.append([tx-1,ty-1])

                    # (tx-1,ty)
                    if tx-1>=0 and img[tx-1][ty]==255 and visited[tx-1][ty]==0:
                        visited[tx-1][ty]=1
                        q.put([tx-1,ty])
                        arc.append([tx-1,ty])

                    # (tx-1,ty+1)
                    if tx-1>=0 and ty+1<cols and img[tx-1][ty+1]==255 and visited[tx-1][ty+1]==0:
                        visited[tx-1][ty+1]=1
                        q.put([tx-1,ty+1])
                        arc.append([tx-1,ty+1])

                    # (tx,ty-1)
                    if ty-1>=0 and img[tx][ty-1]==255 and visited[tx][ty-1]==0:
                        visited[tx][ty-1]=1
                        q.put([tx,ty-1])
                        arc.append([tx,ty-1])

                    # (tx,ty+1)
                    if ty+1<cols and img[tx][ty+1]==255 and visited[tx][ty+1]==0:
                        visited[tx][ty+1]=1
                        q.put([tx,ty+1])
                        arc.append([tx,ty+1])

                    # (tx+1,ty-1)
                    if tx+1<rows and ty-1>=0 and img[tx+1][ty-1]==255 and visited[tx+1][ty-1]==0:
                        visited[tx+1][ty-1]=1
                        q.put([tx+1,ty-1])
                        arc.append([tx+1,ty-1])

                    # (tx+1,ty)
                    if tx+1<rows and img[tx+1][ty]==255 and visited[tx+1][ty]==0:
                        visited[tx+1][ty]=1
                        q.put([tx+1,ty])
                        arc.append([tx+1,ty])

                    # (tx+1,ty+1)
                    if tx+1<rows and ty+1<cols and img[tx+1][ty+1]==255 and visited[tx+1][ty+1]==0:
                        visited[tx+1][ty+1]=1
                        q.put([tx+1,ty+1])
                        arc.append([tx+1,ty+1])

                arcs.append(arc)


    return arcs

# Smooth sub-picture
def getSmoothSmaPlt(sp):
    arcs = getArcs(sp)
    i = 0
    while i < len(arcs):
        arc = arcs[i]

        if len(arc) <= 1:
            arcs.remove(arc)
        else:
            i = i + 1

    tsp = np.zeros((sp.shape[0], sp.shape[1]))
    for i in range(0, len(arcs)):
        arc = arcs[i]
        for j in range(0, len(arc)):
            tx = arc[j][0]
            ty = arc[j][1]

            tsp[tx][ty] = 255

    return tsp

# function: Find the up, down, left, and right four endpoints
def findEdgePoint(img):
    rows=img.shape[0]
    cols=img.shape[1]

    pts=[]

    for i in range(0,rows):
        for j in range(0,cols):
            if img[i,j]==255:
                pts.append([i,j])

    max_i=0    # DOWN
    max_j=0    # RIGHT
    min_i=rows # UP
    min_j=cols # LEFT

    for p in pts:
        tx=p[0]
        ty=p[1]

        if ty<min_j:
            min_j=ty
            left=[tx,ty]

        if tx<min_i:
            min_i=tx
            up=[tx,ty]

        if ty>max_j:
            max_j=ty
            right=[tx,ty]

        if tx>max_i:
            max_i=tx
            down=[tx,ty]

    return [left,up,right,down]

# function:gird-based process
def getSmallkk(bg,sp,k,left,up,right,down):
    fittings=[]

    for i in range(0,sp.shape[0]):
        for j in range(0,sp.shape[1]):
            if sp[i][j]==255:
                tx=i*k
                ty=j*k
                if tx+k<bg.shape[0] and ty+k<bg.shape[1]:
                    kkgrid=np.zeros((k,k))
                    if i>up[0] and j<up[1] and i<left[0] and j>left[1]:# LU
                        # Note the edge points in the grid
                        for m in range(tx,tx+k):
                            for n in range(ty,ty+k):
                                kkgrid[m - tx, n - ty] = bg[m, n]
                        # findtheKeyPts
                        pts=findLUPts(kkgrid,k)
                    elif i>up[0] and j>up[1] and i<right[0] and j<right[1]:# UR
                        for m in range(tx,tx+k):
                            for n in range(ty,ty+k):
                                kkgrid[m - tx, n - ty] = bg[m, n]

                        pts=findURPts(kkgrid,k)
                    elif i>right[0] and j<right[1] and i<down[0] and j>down[1]:# RD
                        for m in range(tx,tx+k):
                            for n in range(ty,ty+k):
                                kkgrid[m - tx, n - ty] = bg[m, n]

                        pts=findRDPts(kkgrid,k)
                    elif i<down[0] and j<down[1] and i>left[0] and j>left[1]:# DL
                        for m in range(tx,tx+k):
                            for n in range(ty,ty+k):
                                kkgrid[m - tx, n - ty] = bg[m, n]

                        pts=findDLPts(kkgrid,k)
                    else:
                        pts=[]
                        for m in range(tx,tx+k):
                            for n in range(ty,ty+k):
                                if bg[m,n]==255:
                                    pts.append([m-tx,n-ty])
                                    kkgrid[m-tx,n-ty]=bg[m,n]

                    fittings.extend(smoothKeyPts(pts,k,tx,ty))

    return fittings

# function: find key points in LU grid
def findLUPts(img,k):
    current=[k,-1]
    pts=[]
    for j in range(current[1]+1,k):
        for i in range(current[0]-1,-1,-1):
            if img[i][j]==255:
                pts.append([i,j])
                current=[i,j]
                break
    return pts

# function: find key points in LU grid
def findURPts(img,k):
    current=[-1,-1]
    pts=[]
    for j in range(current[1]+1,k):
        for i in range(current[0]+1,k):
            if img[i][j]==255:
                pts.append([i,j])
                current=[i,j]
                break
    return pts

# function: find key points in LU grid
def findRDPts(img,k):
    current=[-1,k]
    pts=[]
    for j in range(current[1]-1,-1,-1):
        for i in range(current[0]+1,k):
            if img[i][j]==255:
                pts.append([i,j])
                current=[i,j]
                break

    return pts

# function: find key points in LU grid
def findDLPts(img,k):
    current=[k,k]
    pts=[]
    for j in range(current[1]-1,-1,-1):
        for i in range(current[0]-1,-1,-1):
            if img[i][j]==255:
                pts.append([i,j])
                current=[i,j]
                break

    return pts

# function: find key points in LU grid
def smoothKeyPts(pts,k,tx,ty):
    tmpkk = np.zeros((k, k))
    fittings=[]

    for p in pts:
        tmpkk[p[0], p[1]] = 255

    if k%2==0: # k为偶数
        # Area1
        tmp=calMeans([0,k//2],[0,k//2],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area2
        tmp=calMeans([0,k//2],[k//2,k],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area3
        tmp=calMeans([k//2,k],[0,k//2],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area4
        tmp=calMeans([k//2,k],[k//2,k],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])
    else: # k为奇数
        for m in range(0,k):
            if m!=k//2 and tmpkk[m,k//2]==255:
                fittings.append([m+tx,k//2+ty])

        for m in range(0,k):
            if m!=k//2 and tmpkk[k//2,m]==255:
                fittings.append([k//2+tx,m+ty])

        if tmpkk[k//2,k//2]==255:
            fittings.append([k//2+tx,k//2+ty])

        # Area1
        tmp=calMeans([0,k//2],[0,k//2],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area2
        tmp=calMeans([0,k//2],[k//2+1,k],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area3
        tmp=calMeans([k//2+1,k],[0,k//2],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

        # Area4
        tmp=calMeans([k//2+1,k],[k//2+1,k],tmpkk,tx,ty)
        if tmp[0] is True:
            fittings.append(tmp[1])

    return fittings

# function: Calculate the center of gravity coordinates of grid
def calMeans(xx,yy,kk,tx,ty):
    sum_x=0
    sum_y=0
    num=0

    for m in range(xx[0],xx[1]):
        for n in range(yy[0],yy[1]):
            if kk[m,n]==255:
                sum_x = sum_x + (tx + m)
                sum_y = sum_y + (ty + n)
                num = num + 1
    if num!=0:
        return [True,[sum_x/num,sum_y/num]]
    else:
        return [False]
