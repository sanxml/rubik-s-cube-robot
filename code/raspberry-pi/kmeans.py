import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as p3d

def kmeans(f):
    kmeans_points_list = []
    for line in f.readlines(): #依次读取每行
        line_list = line.strip()
        if not(line_list == ''):
            kmeans_points_list.append(int(line_list)) #去掉每行头尾空白
    points_array=np.array(kmeans_points_list)
    points_array=points_array.reshape(-1,3)
    points = np.float32(points_array)
    print(points[27:36])
    #print(points[9:18])
    # 定义停止标准，应用K均值
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 50, 0.1)
    ret,label,center=cv.kmeans(points,6,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
    print(np.argsort(center,axis=0))
    fig = plt.figure()
    ax = p3d.Axes3D(fig)
    A = points[label.ravel()==0]
    B = points[label.ravel()==1]
    C = points[label.ravel()==2]
    D = points[label.ravel()==3]
    E = points[label.ravel()==4]
    F = points[label.ravel()==5]
    ax.scatter(A[:,0],A[:,1],A[:,2],c = 'b')
    ax.scatter(B[:,0],B[:,1],B[:,2],c = 'r')
    ax.scatter(C[:,0],C[:,1],C[:,2],c = 'm')
    ax.scatter(D[:,0],D[:,1],D[:,2],c = 'c')
    ax.scatter(E[:,0],E[:,1],E[:,2],c = 'g')
    ax.scatter(F[:,0],F[:,1],F[:,2],c = 'y')
    ax.scatter(center[:,0],center[:,1],center[:,2],s = 40,c = 'k', marker = 's')
    plt.show()
f = open('./data/hsv_points.txt',mode='r',encoding='utf-8')
kmeans(f)
