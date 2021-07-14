import sys,os
from PIL import Image



#print(filelist)
def encode(s):
    c = ""
    temp = ""
    for i in s:
        temp = bin(ord(i)).replace('0b','')
        temp = temp.zfill(16)
        c += temp
    length = len(c)
    #print(length)
    if length>65535:
        print("嵌入信息过长！")
        return False
    temp = bin(length+16).replace('0b','')
    temp = temp.zfill(16)#填充16位定长数据长度header
    c = temp + c
    c = '0001100111100010' + c#填入16位定长识别码
    #print(c[:16])
    print("maintain length",len(c))
    return c

'''
水印嵌入算法
使用方法：
flst：作为秘密信息根路径，之后会遍历根目录下的所有子目录名作为秘密信息，尽量避免路径名中出现中文字符
imgpath：载体图片的相对或绝对路径
'''
def embed(flst,imgpath):
#    flst = "E:\\WeChat Files\\WeChat Files\\wxid_2zfm4ix4hkyd22\\FileStorage"
    filelist = ""
    try:
        for root, dirs, files in os.walk(flst, topdown=False):
            for name in dirs:
                #print(os.path.join(root, name))
                filelist += name
    except (PermissionError):
        print("skip this file")


#print(len(filelist))
    filelist = encode(filelist)

    img = Image.open(imgpath)
    img = img.convert("RGB")
#print(filelist)
#print(len(filelist)%16)
#lsb
    codeLen = len(filelist)
    count = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            data = img.getpixel((x, y))
            r = data[0]
            g = data[1]
            b = data[2]
        # 计数器
# 二进制像素值的长度，可以认为要写入图像的文本长度，提取（解密）时也需要此变量
            if count == codeLen:
	            break
            r = (r - r % 2) + int(filelist[count])
        #print(int(filelist[count]),' ',r%2)
            count += 1
            if count == codeLen:
	            img.putpixel((x, y), (r, g, b))
	            break

            g = (g - g % 2) + int(filelist[count])
        #print(int(filelist[count]),' ',g%2)
            count += 1
            if count == codeLen:
	            img.putpixel((x, y), (r, g, b))
	            break

            b = (b - b % 2) + int(filelist[count])
        #print(int(filelist[count]),' ',b%2)
            count += 1
            if count == codeLen:
	            img.putpixel((x, y), (r, g, b))
	            break
# 每3次循环表示一组RGB值被替换完毕，可以进行写入
            if count % 3 == 0:
	            img.putpixel((x, y), (r, g, b))
    img.save('ushiwakamaru_LSB.png')