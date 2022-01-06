# FUNCTION: Tools
import cv2
import numpy as np
import pandas as pd
import math

# function: Write img to xlsx
def writeToxlsx(img,filename):
    data = pd.DataFrame(img)
    writer = pd.ExcelWriter(filename)
    data.to_excel(writer, 'sheet_1', float_format='%.2f')
    writer.save()
    writer.close()

# function: Remove duplicate elements in the list
def remove_Duplicate(lists):
    i=0
    while(i<len(lists)):
        p=lists[i]

        if lists.count(p)>1:
            lists.remove(p)
        else:
            i=i+1

    return lists

# function: Read xlsx file
def readXlsx(filename):
    res=[]
    df=pd.read_excel(filename)

    c=df.columns

    for i in range(0,len(c)):
        try:
            res.append(int(round(c[i])))
        except:
            print(c[i])

    return res

# function: Read parameters from file
def readParasfromtxt(filename):
    paras=[]
    with open(filename,'r') as f:
        lines=f.readlines()
        for line in lines:
            for s in line.split(' '):
                if s is not '':
                    paras.append(float(s))

    return paras

# function: Write and display pictures
def writeAndShow(img,filename):
    # cv2.imshow('aaa',img)
    cv2.imwrite(filename,img)
    # cv2.waitKey(0)

# function: Write parameters to file
def writeResToTxt(res,filename):
    s=str(res[0])+' '+str(res[1])+' '+str(res[3])+' '+str(res[2])+' '+str(res[4])

    with open(filename,'w') as f:
        f.writelines(s)












