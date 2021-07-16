import sys,os
from PIL import Image


'''
水印嵌入算法
使用方法：
flst：作为秘密信息根路径，之后会遍历根目录下的所有子目录名作为秘密信息，尽量避免路径名中出现中文字符
imgpath：载体图片的相对或绝对路径
'''

#默认根目录为用户路径，以列表形式返回根目录下所有的不含中文字符的子文件夹名称
def getFilelist(flst=os.path.expanduser('~')):
    filelist = []
    i = 0
    temp = ''
    try:
        flist = os.listdir(flst)
        for dirs in flist:
            for name in dirs:
                for j in range(len(name)):
                    if ord(name[j])>32 and ord(name[j])<127:
                        temp += name[j]
                #print(os.path.join(root, name))
                #print(name[0])
            if temp != '':
                filelist.append(temp)
            temp = ''
            i += 1
    except (PermissionError):
        print("skip this file")
    return filelist


#将二进制字符串嵌入到载体图像中
def embed(filelist,imgpath):
#    print(filelist)
    img = Image.open(imgpath)
    img = img.convert("RGB")
#    if len(filelist)>imagecapacity(img):
#        print("image is too small to embed the information!")
#        return False
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
    # print("information embeded successfully!")

#返回一张图像可嵌入信息的LSB数量
def imagecapacity(imgpath):
    count = 0
    img = Image.open(imgpath)
    img = img.convert("RGB")
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            count += 3
    return count

#imagecapacity('ushiwakamaru.jpg')
#embed('ushiwakamaru.jpg')
#flst = os.path.expanduser('~')
#filelist = getFilelist()
#print(filelist)
