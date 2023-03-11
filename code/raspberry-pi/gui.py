import tkinter as tk
import cv2 as cv
from PIL import Image,ImageTk
import os
import shutil
import time

import cube
from cube import points_list
import solution
#import kmeans

CAMARA = 1
if CAMARA:
    import ser

exposure = 89
delay_time = 1.8
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv.CAP_PROP_EXPOSURE, exposure)

# 显示图像更新
def video_loop():
    ret, img = camera.read()  # 从摄像头读取照片
    if ret:
        img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)

        # 画魔方轮廓线
        cv.line(img,points_list[0],points_list[1],(0,255,0),3),cv.line(img,points_list[1],points_list[2],(0,255,0),3)
        cv.line(img,points_list[2],points_list[3],(0,255,0),3),cv.line(img,points_list[3],points_list[4],(0,255,0),3)
        cv.line(img,points_list[4],points_list[5],(0,255,0),3),cv.line(img,points_list[5],points_list[0],(0,255,0),3)
        cv.line(img,points_list[1],points_list[4],(0,255,0),3)
        #cv.line(img,(x_point,0),(x_point,360),(0,255,0),3)
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel.imgtk = imgtk
        cube_panel.config(image=imgtk)

        window.after(50, video_loop)
# 绘画六面颜色
def draw_cube():
    color = ['green','red','orange','white','yellow','blue']
    color_ = ['g','r','o','w','y','b']
    canvas = tk.Canvas(window,width=480,height=360,bg="pink")# 创建画布
    for n in range(len(color)):
        col = row = 0
        if (color[n] == 'white'):
            col = 1
            row = 0
        elif (color[n] == 'orange'):
            col = 0
            row = 1
        elif (color[n] == 'green'):
            col = 1
            row = 1
        elif (color[n] == 'red'):
            col = 2
            row = 1
        elif (color[n] == 'blue'):
            col = 3
            row = 1
        elif (color[n] == 'yellow'):
            col = 1
            row = 2

        x=10+col*120;y=10+row*120
        if(os.path.exists('data/'+color[n]+'.txt')):
            if(os.path.exists('data/'+color_[n]+'.txt')):
                f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
            else:
                f = open('data/'+color[n]+'.txt')
            color_list = []
            for line in f.readlines(): #依次读取每行
                color_list.append(line.strip()) #去掉每行头尾空白
            f.close()

            if (len(color_list)==9):
                for i in range(3):
                    for j in range(3):
                        #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                        canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill=str(color_list[i+j*3]),outline='black')
        else:
            for i in range(3):
                for j in range(3):
                    #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                    canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill='pink',outline='black')
    canvas.pack()#包装画布
    canvas.place(relx=0.5, rely=0.1)
# 处理结果并输出
def draw_result():
    #print(time.process_time())
    if CAMARA:
        global camera
        if camera.isOpened():
            camera.release()
        global speed_spin
        #print(speed_spin.get())
        speed_str = 'S'
        speed_str += str(speed_spin.get())
        speed_byte  =  speed_str.encode('utf-8')
        ser.ser_send(speed_byte)
        #print(speed_byte)
        ser.ser_send(b'l')
    
    save_picture()

    if not camera.isOpened():
        camera = cv.VideoCapture(0)
    for n in range(30):
        if(n%2==0):
            gamut_type = 'hsv'
        else:
            gamut_type = 'lab'
        points,label,center,color_dict = cube.kmeans(gamut_type)
        if(cube.check_data() == 1):
            cube.cube_list_sort()
            code_str = solution.code2str()
            step_str,print_str = solution.str2step(code_str)
            send_string = step_str.encode('utf-8')
            if not(len(step_str) == 0):
                print(n)
                #cube.plot(points,label,center,color_dict)
                draw_cube()
                if CAMARA:
                    ser.ser_send(send_string[0:64])
                    t1 = time.process_time()
                    while(time.process_time()<t1+2):
                        pass
                    ser.ser_send(send_string[64:])
                    ser.ser_send(b'c')
                    
                result_lb = tk.Label(window,
                    text=print_str,
                    width=78, height=5,
                    font=('Arial', 12),bg = 'White',)
                result_lb.place(relx = 0,rely = 0.8)
                break
            else:
                color = ['white','red','green','yellow','orange','blue']
                for i in range(6):
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')

# 截图保存图片并处理成数据
def save_picture():
    
    if not CAMARA:
        img = cv.imread('../test/21.png')
        cube.img2points(img)
        img = cv.imread('../test/22.png')
        cube.img2points(img)
        img = cv.imread('../test/23.png')
        cube.img2points(img)

    if CAMARA:   
        for i in range(3):
            camera = cv.VideoCapture(0)
            ret, img = camera.read()
            img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
            camera.release()
            cube.img2points(img)
            cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
            ser.ser_send(b'XzC')
            if(i<2):
                t0 = time.process_time()
                while(time.process_time()<t0+delay_time):
                    pass
            
            
        
        #global camera
        #
        #camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
        #camera.set(cv.CAP_PROP_EXPOSURE, exposure)
        
        #camera.set(cv.CAP_PROP_EXPOSURE, exposure)
        
        
        
        
        

def reset():
    if CAMARA:
        ser.ser_send(b'c')
        global camera
        if not camera.isOpened():
            camera = cv.VideoCapture(0)

    shutil.rmtree('./data')
    os.mkdir('./data')
    shutil.rmtree('./picture')
    os.mkdir('./picture')
    draw_cube()
    result_lb = tk.Label(window,
        text='',
        width=78, height=5,
        font=('Arial', 12),bg = 'white',)
    result_lb.place(relx = 0,rely = 0.8)

    result_lb = tk.Label(window,
    text='等待点击运行按钮。。。',
    width=78, height=5,
    font=('Arial', 12),bg = 'White',)
    result_lb.place(relx = 0,rely = 0.8)


if (os.path.exists('./data')):
    shutil.rmtree('./data')
os.mkdir('./data')
if (os.path.exists('./picture')):
    shutil.rmtree('./picture')
os.mkdir('./picture')

window = tk.Tk()
window.title("魔方机器人")
window.geometry("1024x600")

#调用摄像头
if CAMARA:
    ser.ser_init()
    cube_panel = tk.Label(window)
    cube_panel.place(relx = 0.02,rely = 0.1)
    video_loop()

draw_cube()

run_btn = tk.Button(window,
    text='运行',      # 显示在按钮上的文字
    width=10, height=2,
    font=('Arial', 12),bg = 'Pink',
    command=draw_result)   # 点击按钮式执行的命令
run_btn.place(relx = 0.8,rely = 0.9)    # 按钮位置

picture_btn = tk.Button(window,
    text='复位',      # 显示在按钮上的文字
    width=10, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=reset)   # 点击按钮式执行的命令
picture_btn.place(relx = 0.7,rely = 0.9)    # 按钮位置

result_lb = tk.Label(window,
    text='等待点击运行按钮。。。',
    width=78, height=5,
    font=('Arial', 12),bg = 'White',)
result_lb.place(relx = 0,rely = 0.8)

speed_lb = tk.Label(window,
    text='速度：',
    width=6,
    font=('Arial', 14))
speed_lb.place(relx = 0.75,rely = 0.8)

var = tk.IntVar()
var.set(48)
speed_spin = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var)
speed_spin.place(relx = 0.82,rely = 0.8)

window.mainloop()

# 当一切都完成后，关闭摄像头并释放所占资源
if CAMARA:
    camera.release()
    ser.ser_close()
cv.destroyAllWindows()