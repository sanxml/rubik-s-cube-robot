import os
import time
import cv as cv
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as p3d

x_point=150; y_point=75 ;mid_point=35
points_list = [(x_point,y_point),(260,mid_point),(515-x_point,y_point),(515-x_point,305-y_point),(260,300-mid_point),(x_point,305-y_point)]
# 轮廓处理和图片矫正及分割
def contour_process(in_img,out_img_shape):
    # 左右图分割和文档矫正
    left_last_points = np.float32([points_list[0],points_list[1],points_list[5],points_list[4]])
    right_last_points = np.float32([points_list[1],points_list[2],points_list[4],points_list[3]])
    new_points = np.float32([[0,0],[out_img_shape[0],0],[0,out_img_shape[1]],[out_img_shape[0],out_img_shape[1]]])
    ML = cv.getPerspectiveTransform(left_last_points,new_points)
    left_img = cv.warpPerspective(in_img,ML,(out_img_shape[0],out_img_shape[1]))
    MR = cv.getPerspectiveTransform(right_last_points,new_points)
    right_img = cv.warpPerspective(in_img,MR,(out_img_shape[0],out_img_shape[1]))

    return left_img, right_img
# 魔方颜色序列调整
def cube_list_sort():
    f = open('data/sort.txt',mode='r',encoding='utf-8')
    sort_str = f.read(2)
    case = -1
    # print(sort_list)
    if(sort_str == 'gw' or sort_str == 'yr' or sort_str == 'ob'):
        case = 0
    elif(sort_str == 'gr' or sort_str == 'oy' or sort_str == 'wb'):
        case = 1
    elif(sort_str == 'go' or sort_str == 'rw' or sort_str == 'yb'):
        case = 2
    elif(sort_str == 'gy' or sort_str == 'wo' or sort_str == 'rb'):
        case = 3
    elif(sort_str == 'wg' or sort_str == 'ry' or sort_str == 'bo'):
        case = 4
    elif(sort_str == 'rg' or sort_str == 'yo' or sort_str == 'bw'):
        case = 5
    elif(sort_str == 'og' or sort_str == 'wr' or sort_str == 'by'):
        case = 6
    elif(sort_str == 'yg' or sort_str == 'ow' or sort_str == 'br'):
        case = 7
    # print(case)
    # 不变，顺时针，逆时针，倒转
    sort_way = [[0,1,2,3,4,5,6,7,8],[6,3,0,7,4,1,8,5,2],[2,5,8,1,4,7,0,3,6],[8,7,6,5,4,3,2,1,0]]
    sort_case = [[2,2,2,0,3,3],[2,0,0,0,1,1],[3,2,3,1,3,2],[3,0,1,1,1,0],[1,1,1,3,0,0],[1,3,3,3,2,2],[0,1,0,2,0,1],[0,3,2,2,2,3]]


    color = ['white','red','green','yellow','orange','blue']
    color_ = ['w','r','g','y','o','b']

    for i in range(len(color)):
        f = open('data/'+color[i]+'.txt',mode='r',encoding='utf-8')
        color_list = []
        rule_list = []
        for line in f.readlines(): #依次读取每行
            lines = line.strip()
            rule_list.append(lines) #去掉每行头尾空白
        # print(rule_list)
        for j in sort_way[sort_case[case][i]]:
            color_list.append(str(rule_list[j]))
        # print(color_list)
        f.close()
        f = open('data/'+color_[i]+'.txt',mode='w',encoding='utf-8')
        # print(color_[i])
        for i in range(len(color_list)):
            f.write(color_list[i])
            f.write('\n')
        f.close()
# 图片矫正并保存为每个点的值
def img2points(img):
    left_img,right_img = contour_process(img,[30,30])
    #cv.imwrite('./picture/'+str(time.process_time())+'left_img'+'.png',left_img)
    #cv.imwrite('./picture/'+str(time.process_time())+'right_img'+'.png',right_img)

    hsv_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2HSV)
    hsv_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2HSV)

    lab_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2LAB)
    lab_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2LAB)


    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    for i in range(int(hsv_left_img.shape[0]/6),int(hsv_left_img.shape[0]),int(hsv_left_img.shape[0]/3)):
        for j in range(int(hsv_left_img.shape[1]/6),int(hsv_left_img.shape[1]),int(hsv_left_img.shape[1]/3)):
            f.write(str(hsv_left_img[i,j][0])+'\n')
            f.write(str(hsv_left_img[i,j][1])+'\n')
            f.write(str(hsv_left_img[i,j][2])+'\n\n')
    for i in range(int(hsv_right_img.shape[0]/6),int(hsv_right_img.shape[0]),int(hsv_right_img.shape[0]/3)):
        for j in range(int(hsv_right_img.shape[1]/6),int(hsv_right_img.shape[1]),int(hsv_right_img.shape[1]/3)):
            f.write(str(hsv_right_img[i,j][0])+'\n')
            f.write(str(hsv_right_img[i,j][1])+'\n')
            f.write(str(hsv_right_img[i,j][2])+'\n\n')
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    for i in range(int(lab_left_img.shape[0]/6),int(lab_left_img.shape[0]),int(lab_left_img.shape[0]/3)):
        for j in range(int(lab_left_img.shape[1]/6),int(lab_left_img.shape[1]),int(lab_left_img.shape[1]/3)):
            f.write(str(lab_left_img[i,j][0])+'\n')
            f.write(str(lab_left_img[i,j][1])+'\n')
            f.write(str(lab_left_img[i,j][2])+'\n\n')
    for i in range(int(lab_right_img.shape[0]/6),int(lab_right_img.shape[0]),int(lab_right_img.shape[0]/3)):
        for j in range(int(lab_right_img.shape[1]/6),int(lab_right_img.shape[1]),int(lab_right_img.shape[1]/3)):
            f.write(str(lab_right_img[i,j][0])+'\n')
            f.write(str(lab_right_img[i,j][1])+'\n')
            f.write(str(lab_right_img[i,j][2])+'\n\n')
    f.close()

# K-Means聚类颜色识别
def kmeans(gamut_type):
    kmeans_points_list = []
    f = open('./data/'+gamut_type+'_points.txt',mode='r',encoding='utf-8')
    for line in f.readlines(): #依次读取每行
        line_list = line.strip()
        if not(line_list == ''):
            kmeans_points_list.append(int(line_list)) #去掉每行头尾空白
    points_array=np.array(kmeans_points_list)
    points_array=points_array.reshape(-1,3)
    points = np.float32(points_array)
    # print(points)

    # 定义停止标准，应用K均值
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1)
    ret,label,center=cv.kmeans(points,6,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
#     print(type(label))
#     print(type(center))
    color_dict = {}
    if(gamut_type=='lab'):
        wo_temp = []
        for i in range(6):
            if (i == np.argsort(center,axis=0)[0][0]):
                color_dict['red'] = i
            elif(i == np.argsort(center,axis=0)[1][0]):
                color_dict['blue'] = i
            elif(i == np.argsort(center,axis=0)[0][1]):
                color_dict['green'] = i
            elif(i == np.argsort(center,axis=0)[1][1]):
                color_dict['yellow'] = i
            else:
                wo_temp.append(i)

        for i in range(6):
            if(wo_temp[0] == np.argsort(center,axis=0)[i][2]):
                color_dict['white'] = wo_temp[1]
                color_dict['orange'] = wo_temp[0]
                break
            elif(wo_temp[1] == np.argsort(center,axis=0)[i][2]):
                color_dict['orange'] = wo_temp[1]
                color_dict['white'] = wo_temp[0]
                break
    #print(color_dict)
    elif(gamut_type=='hsv'):
        gy_temp = []
        for i in range(6):
            if (i == np.argsort(center,axis=0)[0][0]):
                color_dict['blue'] = i
            elif(i == np.argsort(center,axis=0)[1][0]):
                color_dict['white'] = i
            elif(i == np.argsort(center,axis=0)[2][0]):
                color_dict['green'] = i
            elif(i == np.argsort(center,axis=0)[3][0]):
                color_dict['yellow'] = i
            elif(i == np.argsort(center,axis=0)[4][0]):
                color_dict['orange'] = i
            elif(i == np.argsort(center,axis=0)[5][0]):
                color_dict['red'] = i
        # for i in range(6):
        #     if (i == np.argsort(center,axis=0)[0][1]):
        #         color_dict['white'] = i
        #     elif(i == np.argsort(center,axis=0)[0][0]):
        #         color_dict['blue'] = i
        #     elif(i == np.argsort(center,axis=0)[5][2]):
        #         color_dict['orange'] = i
        #     elif(i == np.argsort(center,axis=0)[5][0]):
        #         color_dict['red'] = i
        #     else:
        #         gy_temp.append(i)
        # for i in range(6):
        #     if(gy_temp[0] == np.argsort(center,axis=0)[i][0]):
        #         color_dict['green'] = gy_temp[0]
        #         color_dict['yellow'] = gy_temp[1]
        #         break
        #     elif(gy_temp[1] == np.argsort(center,axis=0)[i][0]):
        #         color_dict['green'] = gy_temp[1]
        #         color_dict['yellow'] = gy_temp[0]
        #         break
    #print(color_dict)

    if(len(color_dict) == 6):
        for p in range(6):
            if(label[p*9+4] == color_dict['blue']):
                title_str = "blue"
            elif(label[p*9+4] == color_dict['red']):
                title_str = "red"
            elif(label[p*9+4] == color_dict['orange']):
                title_str = "orange"
            elif(label[p*9+4] == color_dict['white']):
                title_str = "white"
            elif(label[p*9+4] == color_dict['green']):
                title_str = "green"
            elif(label[p*9+4] == color_dict['yellow']):
                title_str = "yellow"
            f = open('./data/sort.txt',mode='a',encoding='utf-8')
            f.write(title_str[0])
            f.close()
            f = open('./data/'+title_str+'.txt',mode='a',encoding='utf-8')
            for i in range(9):
                if(label[p*9+i] == color_dict['blue']):
                    color_str = "blue\n"
                elif(label[p*9+i] == color_dict['red']):
                    color_str = "red\n"
                elif(label[p*9+i] == color_dict['orange']):
                    color_str = "orange\n"
                elif(label[p*9+i] == color_dict['white']):
                    color_str = "white\n"
                elif(label[p*9+i] == color_dict['green']):
                    color_str = "green\n"
                elif(label[p*9+i] == color_dict['yellow']):
                    color_str = "yellow\n"
                f.write(color_str)
            f.close()
    return points, label, center, color_dict
    # print(center)
    # print(color_dict)
    # print(np.argsort(center,axis=0))

# 绘制数据
def plot(points, label, center, color_dict):
    fig = plt.figure()
    ax = p3d.Axes3D(fig)
    A = points[label.ravel()==color_dict['blue']]
    B = points[label.ravel()==color_dict['red']]
    C = points[label.ravel()==color_dict['orange']]
    D = points[label.ravel()==color_dict['white']]
    E = points[label.ravel()==color_dict['green']]
    F = points[label.ravel()==color_dict['yellow']]
    ax.scatter(A[:,0],A[:,1],A[:,2],c = 'b')
    ax.scatter(B[:,0],B[:,1],B[:,2],c = 'r')
    ax.scatter(C[:,0],C[:,1],C[:,2],c = 'm')
    ax.scatter(D[:,0],D[:,1],D[:,2],c = 'c')
    ax.scatter(E[:,0],E[:,1],E[:,2],c = 'g')
    ax.scatter(F[:,0],F[:,1],F[:,2],c = 'y')
    ax.scatter(center[:,0],center[:,1],center[:,2],s = 40,c = 'k', marker = 's')
    plt.show()

#kmeans()

def check_data():
    color = ['white','red','green','yellow','orange','blue']
    if (os.path.exists('./data/blue.txt') and os.path.exists('./data/green.txt') and
        os.path.exists('./data/red.txt') and os.path.exists('./data/orange.txt') and
        os.path.exists('./data/white.txt') and os.path.exists('./data/yellow.txt')):
        for j in range(6):
            if(j == 5):
                return 1
            num = 0
            for i in range(len(color)):
                f = open('data/'+color[i]+'.txt',mode='r',encoding='utf-8')
                for line in f.readlines(): #依次读取每行
                    lines = line.strip()
                    if(lines == color[j]):
                        num += 1
                        # print(num)
            if(num == 9):
                continue
            else:
                for i in range(6):
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                break
    else:
        for i in range(6):
            if os.path.exists('data/sort.txt'):
                os.remove('data/sort.txt')
            if os.path.exists('data/'+color[i]+'.txt'):
                os.remove('data/'+color[i]+'.txt')
        return 0

# print(check_data())

def check_light(img):
    img = cv.imread('3.png')
    # 把图片转换为单通道的灰度图
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 获取形状以及长宽
    img_shape = gray_img.shape
    height, width = img_shape[0], img_shape[1]
    size = gray_img.size
    # 灰度图的直方图
    hist = cv.calcHist([gray_img], [0], None, [256], [0, 256])
    # 计算灰度图像素点偏离均值(128)程序
    a = 0
    ma = 0
    #np.full 构造一个数组，用指定值填充其元素
    reduce_matrix = np.full((height, width), 128)
    shift_value = gray_img - reduce_matrix
    shift_sum = np.sum(shift_value)
    da = shift_sum / size
    # 计算偏离128的平均偏差
    for i in range(256):
        ma += (abs(i-128-da) * hist[i])
    m = abs(ma / size)
    # 亮度系数
    k = abs(da) / m
    print(k)
return k
# if k[0] > 1:
#     # 过亮
#     if da > 0:
#         print("过亮")
#     else:
#         print("过暗")
# else:
#     print("亮度正常")