from PIL import Image
import sys,os

#水印提取算法
'''
使用方法：只需要将含密图片的相对或绝对路径作为输入参数，
直接调用即可提取出内含的秘密信息
'''
def extract(imgpath):
    im = Image.open(imgpath)
    im = im.convert("RGB")
    width=im.size[0]
    height=im.size[1]
    length = 10086
#print("下",int(filelist[0:16],2))
#print("下",filelist[0:16])
#计数器
    count= 0
    wt=""
    certificate = ""
    for i in range(width):
        for j in range(height):
        # 获取像素点的值
            rgb = im.getpixel((i, j))
        # 提取R通道的附加值
            if count % 3 == 0:
                wt = wt + str(rgb[0] % 2)
                if count == length:
                    break
                count += 1
            #print(rgb[0]%2)
            if count == 16:
                certificate = wt[:16]
                if certificate != '0001100111100010':
                    print("This is not a target image! Extract progress terminated!")
                    return False
            #print("r",wt[:16])
            #print("提取长度",length)
                wt = ""
    # 提取G通道的附加值
            if count % 3 == 1:
                wt = wt + str(rgb[1] % 2)
            #print(rgb[1]%2)
                if count == length:
                    break
                count += 1
            if count == 32:
                length = int(wt[:16],2)
            #print("g",wt[:16])
                print("提取长度",length)
                wt = ""

    # 提取B通道的附加值
            if count % 3 == 2:
                wt = wt + str(rgb[2] % 2)
            #print(rgb[2]%2)
                if count == length:
                    break
                count += 1
            if count == 16:
                length = int(wt[:15],2)
            #print("b",wt[:16])
            #print("提取长度",length)
                wt = ""

#    print(count,' ',length,' ',len(wt))
    temp = 0
    content = ""
    for i in range(0,length-32,16):
        temp = chr(int(wt[i:i+16],2))
    #print(chr(int(wt[i:i+16])))
    #print(wt[i:i+16])
        content+=temp
    #print("提取内容",content)
    print("提取成功！")
    restore = open('content1.txt',mode = 'a',encoding = 'UTF-8')
    restore.write(content)
    restore.close()
extract('ushimaru_LSB.png')