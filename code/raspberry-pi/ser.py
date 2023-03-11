import serial
import time

#def main():
#    while True:
#        # 获得接收缓冲区字符
#        count = ser.inWaiting()
#        if count != 0:
#            # 读取内容并显示
#            recv = ser.read(count)
#            print(recv)
#        # 清空接收缓冲区
#        ser.flushInput()
#        # 必要的软件延时
#        time.sleep(0.1)
#
#if __name__ == '__main__':
#    try:
#    # 打开串口
#        ser = serial.Serial('/dev/ttyAMA0', 115200)
#        if ser.isOpen == False:
#            ser.open()                # 打开串口
#        ser.write(b"rRZzXfxFRRXX")
#        #ser.write(b"rzrzRRzRzFZZrZZxfxFXXrZRzRzrZFFzRZRRFFxfxFFXXZZRRZrzRR")
#        main()
#    except KeyboardInterrupt:
#        if ser != None:
#            ser.close()
arduino_ser = serial.Serial('/dev/ttyAMA0', 115200)

def ser_init():
    if arduino_ser.isOpen == False:
        arduino_ser.open()                # 打开串口

def ser_close():
    if arduino_ser != None:
        arduino_ser.close()

def ser_send(string):
    arduino_ser.write(string)


def ser_recv():
    while True:
        # 获得接收缓冲区字符
        count = arduino_ser.inWaiting()
        # 读取内容并显示
        if count == 0:
            break
        recv = arduino_ser.read(count)
        print(recv)
        # 清空接收缓冲区
        arduino_ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
        return recv
