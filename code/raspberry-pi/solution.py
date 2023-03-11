import kociemba as kc

# 颜色列表转魔方序列列表
def color2code(line_list):
    # U R F D L B
    # 白 红 绿 黄 橙 蓝
    if (line_list == 'white'):
        line_list = 'U'
    elif (line_list == 'yellow'):
        line_list = 'D'
    elif (line_list == 'green'):
        line_list = 'F'
    elif (line_list == 'orange'):
        line_list = 'L'
    elif (line_list == 'red'):
        line_list = 'R'
    elif (line_list == 'blue'):
        line_list = 'B'
    else:
        line_list = 'N'
    return line_list
# 魔方序列列表转字符串
def code2str():
    color_ = ['w','r','g','y','o','b']
    color_list = []
    for n in range(len(color_)):
        f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
        for line in f.readlines(): #依次读取每行
            line_list = line.strip()
            color_list.append(color2code(line_list)) #去掉每行头尾空白
    code_str = ''
    for i in range(len(color_list)):
        code_str += color_list[i]
    # print(code_str)
    return code_str
# 魔方字符串转电机字符串
def str2step(code_str):
    copy_list = list(code_str)
    i = 0
    while(i < len(copy_list)-1):
        if(copy_list[i] == copy_list[i+1]):
            del copy_list[i]
        else:
            i+=1
    if not(len(copy_list) == 6):
        #print(code_str)
        try:
            kc_str = kc.solve(code_str)
            kc_flag = 0
        except:
            kc_str = ''
    else:
        kc_str = ''
    # print('六面最佳解法： '+ kc_str)
    #print(sort_str)

    cube_str = ''
    for i in range(len(kc_str)):
        if(kc_str[i] != ' '):
            if(kc_str[i] == '2'):
                cube_str += kc_str[i-1]
            elif(kc_str[i] == "'"):
                cube_str = cube_str[:len(cube_str)-1]
                cube_str += kc_str[i-1].lower()
            else:
                cube_str += kc_str[i]

    #print(cube_str)
    step_list = []
    for loop_num in range(12):
        step_str = ''
        for i in range(len(cube_str)):
            if(cube_str[i] == 'R'):
                step_str += 'R'
            elif(cube_str[i] == 'r'):
                step_str += 'r'
            elif(cube_str[i] == 'L'):
                step_str += 'ZZRZZ'
            elif(cube_str[i] == 'l'):
                step_str += 'ZZrZZ'
            elif(cube_str[i] == 'U'):
                if(loop_num >= 8):
                    step_str += 'ZRz'
                else:
                    step_str += 'xFX'
            elif(cube_str[i] == 'u'):
                if(loop_num%8 >= 4):
                    step_str += 'Zrz'
                else:
                    step_str += 'xfX'
            elif(cube_str[i] == 'D'):
                if(loop_num%4 >= 2):
                    step_str += 'zRZ'
                else:
                    step_str += 'XFx'
            elif(cube_str[i] == 'd'):
                if(loop_num%2):
                    step_str += 'zrZ'
                else:
                    step_str += 'Xfx'
            elif(cube_str[i] == 'F'):
                step_str += 'F'
            elif(cube_str[i] == 'f'):
                step_str += 'f'
            elif(cube_str[i] == 'B'):
                step_str += 'XXFXX'
            elif(cube_str[i] == 'b'):
                step_str += 'XXfXX'
        
        f = open('data/sort.txt',mode='r',encoding='utf-8')
        sort_str = f.read(2)
        f.close()
        if(sort_str == 'ob'):
            step_str += ' '
        elif(sort_str == 'ow'):
            step_str = "x" + step_str
        elif(sort_str == 'og'):
            step_str = "XX" + step_str
        elif(sort_str == 'oy'):
            step_str = "X" + step_str

        elif(sort_str == 'rb'):
            step_str = "ZZ" + step_str
        elif(sort_str == 'rw'):
            step_str = "ZZx" + step_str
        elif(sort_str == 'rg'):
            step_str = "ZZXX" + step_str
        elif(sort_str == 'ry'):
            step_str = "xZZ" + step_str

        elif(sort_str == 'yb'):
            step_str = "z" + step_str
        elif(sort_str == 'yo'):
            step_str = "xz" + step_str
        elif(sort_str == 'yg'):
            step_str = "XXz" + step_str
        elif(sort_str == 'yr'):
            step_str = "Xz" + step_str

        elif(sort_str == 'wb'):
            step_str = "Z" + step_str
        elif(sort_str == 'wo'):
            step_str = "XZ" + step_str
        elif(sort_str == 'wg'):
            step_str = "XXZ" + step_str
        elif(sort_str == 'wr'):
            step_str = "xZ" + step_str

        elif(sort_str == 'go'):
            step_str = "xzX" + step_str
        elif(sort_str == 'gy'):
            step_str = "zX" + step_str
        elif(sort_str == 'gr'):
            step_str = "xZx" + step_str
        elif(sort_str == 'gw'):
            step_str = "Zx" + step_str

        elif(sort_str == 'br'):
            step_str = "xZX" + step_str
        elif(sort_str == 'bw'):
            step_str = "zx" + step_str
        elif(sort_str == 'bo'):
            step_str = "XZX" + step_str
        elif(sort_str == 'by'):
            step_str = "ZX" + step_str

        # print(step_str)

        step_str_0 = ''
        step_str_cp = step_str
        for n in range(6):
            step_str_0 = ''
            for i in range(len(step_str_cp)):
                if(len(step_str_cp)>2):
                    step_str_0 += step_str_cp[i]
                    if((step_str_cp[i-1] == 'X' or step_str_cp[i-1] == 'x') and
                    (step_str_cp[i] == 'R' or step_str_cp[i-1] == 'r')):
                        temp_str = step_str_cp[i-1]
                        step_str_0 = step_str_0[:len(step_str_0)-2] + step_str_0[len(step_str_0)-1:len(step_str_0)]
                        step_str_0 += temp_str
                    elif((step_str_cp[i-1] == 'Z' or step_str_cp[i-1] == 'z') and
                    (step_str_cp[i] == 'F' or step_str_cp[i-1] == 'f')):
                        temp_str = step_str_cp[i-1]
                        step_str_0 = step_str_0[:len(step_str_0)-2] + step_str_0[len(step_str_0)-1:len(step_str_0)]
                        step_str_0 += temp_str
                else:
                    step_str_0 = step_str_cp
            step_str_cp = step_str_0


        # print(step_str_0)
        # print(" ")
        step_str_cp = step_str_0
        for n in range(6):
            step_str_1 = ''
            for i in range(len(step_str_cp)):
                if(len(step_str_cp)>3):
                    if(step_str_cp[i-3] == 'Z' and step_str_cp[i-2] == 'Z' and
                    step_str_cp[i-1] == 'Z' and step_str_cp[i] == 'Z' and i > 3):
                        step_str_1 = step_str_1[:len(step_str_1)-3]
                    elif(step_str_cp[i-3] == 'X' and step_str_cp[i-2] == 'X' and
                    step_str_cp[i-1] == 'X' and step_str_cp[i] == 'X' and i > 3):
                        step_str_1 = step_str_1[:len(step_str_1)-3]
                    else:
                        step_str_1 += step_str_cp[i]
                else:
                    step_str_1 = step_str_cp
            # print(step_str_1)

            step_str_2 = ''
            for i in range(len(step_str_1)):
                if(len(step_str_1)>2):
                    if(step_str_1[i-2] == 'Z' and step_str_1[i-1] == 'Z' and
                    step_str_1[i] == 'Z' and i > 2):
                        step_str_2 = step_str_2[:len(step_str_2)-2]
                        step_str_2 += 'z'
                    elif(step_str_1[i-2] == 'X' and step_str_1[i-1] == 'X' and
                    step_str_1[i] == 'X' and i > 2):
                        step_str_2 = step_str_2[:len(step_str_2)-2]
                        step_str_2 += 'x'
                    else:
                        step_str_2 += step_str_1[i]
                else:
                    step_str_2 = step_str_1
            # print(step_str_2)

            step_str_3 = ''
            for i in range(len(step_str_2)):
                if(len(step_str_2)>1):
                    if((step_str_2[i-1] == 'x' and step_str_2[i] == 'X' and i > 1) or
                    (step_str_2[i-1] == 'X' and step_str_2[i] == 'x' and i > 1) or
                    (step_str_2[i-1] == 'z' and step_str_2[i] == 'Z' and i > 1) or
                    (step_str_2[i-1] == 'Z' and step_str_2[i] == 'z' and i > 1)):
                        step_str_3 = step_str_3[:len(step_str_3)-1]
                    else:
                        step_str_3 += step_str_2[i]
                else:
                    step_str_3 = step_str_2
            # print(step_str_3)

            step_str_4 = ''
            for i in range(len(step_str_3)):
                if(len(step_str_3)>2):
                    step_str_4 += step_str_3[i]
                    if((step_str_3[i-1] == 'X' or step_str_3[i-1] == 'x') and
                    (step_str_3[i] == 'R' or step_str_3[i-1] == 'r')):
                        temp_str = step_str_3[i-1]
                        step_str_4 = step_str_4[:len(step_str_4)-2] + step_str_4[len(step_str_4)-1:len(step_str_4)]
                        step_str_4 += temp_str
                    elif((step_str_3[i-1] == 'Z' or step_str_3[i-1] == 'z') and
                    (step_str_3[i] == 'F' or step_str_3[i-1] == 'f')):
                        temp_str = step_str_3[i-1]
                        step_str_4 = step_str_4[:len(step_str_4)-2] + step_str_4[len(step_str_4)-1:len(step_str_4)]
                        step_str_4 += temp_str
                else:
                    step_str_4 = step_str_3

                #print(step_str_4)
            step_str_cp = step_str_4


        step_str_end = ''
        end_index = 0
        for i in range(len(step_str_4)-1,-1,-1):
            if(step_str_4[i] == 'R' or step_str_4[i] == 'r' or
            step_str_4[i] == 'F' or step_str_4[i] == 'f'):
                end_index = i + 1
                break
        step_str_end = step_str_4[:end_index]
        # print(step_str_end)

        step_list.append(step_str_end)

    # print(step_list)
    step_str = step_list[0]
    for i in range(len(step_list)):
        if(len(step_str) > len(step_list[i])):
            step_str = step_list[i]

    #验证
    test_str = ''
    for i in range(len(step_str)):
        if(step_str[i] == 'r'):
            test_str += "R'"
        elif(step_str[i] == 'f'):
            test_str += "F'"
        elif(step_str[i] == 'z'):
            test_str += "Z'"
        elif(step_str[i] == 'x'):
            test_str += "X'"
        else:
            test_str += step_str[i]
    print_str = '六面解法： '+ kc_str + '\n两面解法: \n'+test_str + '\n共'+str(len(step_str))+'步'
    # print('step_str_1: '+step_str_1)
    # print('step_str_2: '+step_str_2)
    # print('step_str_3: '+step_str_3)
    # print('step_str_4: '+step_str_4)
    # print('step_str_end: '+step_str_end)
    print('step_str: '+step_str)
    #print(len(step_str))
    return step_str, print_str
