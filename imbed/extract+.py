from PIL import Image
import sys,os

#水印提取算法
'''
使用方法：只需要将含密图片的相对或绝对路径作为输入参数，输入开始位置与
直接调用即可提取出内含的秘密信息比特流
'''

def extract(imgpath,begin,length):
    im = Image.open(imgpath)
    im = im.convert("RGB")
    width=im.size[0]
    height=im.size[1]
#计数器
    count= 0
    wt=""
    flag = 0
    for i in range(width):
        for j in range(height):
        # 获取像素点的值
            rgb = im.getpixel((i, j))
        # 提取R通道的附加值
            if count % 3 == 0 and count>=begin:
                if count >= begin+length:
                    flag = 1
                    break
                wt = wt + str(rgb[0] % 2)
            count += 1
            #print(count,begin)
            #print(rgb[0]%2)
            #检验图像是否含有秘密信息
            #if count == 16:
            #    certificate = wt[:16]
            #    if certificate != '0001100111100010':
            #        print("This is not a target image! Extract progress terminated!")
            #        return False
            #print("r",wt[:16])
            #print("提取长度",length)
#                wt = ""
    # 提取G通道的附加值
            if count % 3 == 1 and count>=begin:
                if count >= begin+length:
                    flag = 1
                    break
                wt = wt + str(rgb[1] % 2)
            #print(rgb[1]%2)
                
            count += 1
            #print(count,begin)
            #if count == 32:
            #    length = int(wt[:16],2)
            #    print("g",wt[:16])
            #    print("提取长度",length)
            #    wt = ""

    # 提取B通道的附加值
            if count % 3 == 2 and count>=begin:
                if count >= begin+length:
                    flag = 1
                    break
                wt = wt + str(rgb[2] % 2)
            #print(rgb[2]%2)
            count += 1
            #print(count,begin)
            #提取长度
            #if count == 16:
            #    length = int(wt[:16],2)
            #    print("b",wt[:16])
            #    print("提取长度",length)
            #    wt = ""
        if flag == 1:
            break

#    print(count,' ',length,' ',len(wt),begin)
    print("提取成功！")
    return wt
#begin = 28
#length = 8
#wt = extract('ushiwakamaru_LSB.png',begin,length)
#print(wt)
