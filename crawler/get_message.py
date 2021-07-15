import re_crawler
import os
import extracttool
import trans
from functools import cmp_to_key

# 定长首部 一共56bit     
# ==================================    
# 序号字段8 bit,从0开始,序号全1表示无分片    
num=8
# 同一类码 8 bit    
kindLen=20    
# 当前嵌入长度字段 20bit    
lenght_seg=20    
# 嵌入了信息的标志 8 bit    
symbol="11000000"    
# ==================================

allowext=('.png')

def generate_message(kindmap):
    """
        同类字典，存储图片路径 得到一个包含秘密信息的txt文件
    """
    def func(x,y):
       """ 
            传入的是图片名字符串
       """
       a=extracttool.extract(x,28,8)
       b=extracttool.extract(y,28,8)
       a=int(a,2)
       b=int(b,2)
       if a <b:
           return -1
       if a==b:
           return 0
       else :
           return 1
       
    for k in kindmap:
        kindmap[k]=sorted(kindmap[k],key=cmp_to_key(func))
    
    message=""
    for k in kindmap:
        tmp=""
        for img in kindmap[k]:
            length=extracttool.extract(img,8,20)    
            # print(int(extracttool.extract(img,28,8),2))  
            length=int(length,2)
            tmp+=extracttool.extract(img,56,length)
        tmp=tmp[0:len(tmp)//8*8]
        message+=trans.Str_decode(tmp)+"\nkind:{}\n\n".format(k)

    with open('data.txt','a') as f:
        f.write(message)
    print("Finish")
if __name__=="__main__":
    url="http://192.168.43.137:5000/"
    store_path="img/"
    # 同类map,同一类码:图片路径, 列表
    kindmap={}

    # 爬取到本地
    re_crawler.crawler(url=url,store_path=store_path)
    pics=os.listdir(store_path)
    for p in pics:
        path=os.path.join(store_path,p)
        name,ext=os.path.splitext(path)
        # print(ext)
        if ext.lower() in allowext:
            # 拿到header
            header=""
            try :
                header=extracttool.extract(path,0,56)
            except Exception:
                print("容量 may too short.")
                continue
            if header[0:len(symbol)] ==symbol:
                #有
                # 得到同一类码 ,得到一个字典
                kind=int(header[36:56],2)
                if kind in kindmap.keys():
                    kindmap[kind]+=[path]
                else :
                    kindmap[kind]=[path] 
    generate_message(kindmap)
