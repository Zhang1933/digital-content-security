import os
import rsa
import time
import sys,getopt
import base64
import json
import requests
import embedTool
import trans

# 构造包分片
# 定长首部 一共56bit 
# ==================================
# 序号字段8 bit,从0开始,序号全1表示无分片
numLen=8
# 同一类码 8 bit
kindLen=20
# 当前嵌入长度字段 20bit
typelenght=20
# 嵌入了信息的标志 8 bit
symbol="11000000"
# ==================================


def help():
    print("Usage: {} -r [服务器地址] -m [上传图片的文件路径] -n [你的公钥n] -e [你的公钥e] -u [你的邮箱] -p [你的密码]".format(__file__))
    print("{} -h: Show this help message".format(__file__))

def image_to_64b(image_file):
    """
        将图片转为base64
    """
    with open(image_file,"rb") as f:
        im_bytes=f.read()
    return base64.b64encode(im_bytes).decode("utf8")



def send_json(url,email,encryppass,im_b64):
    """
        发送json 文件post表单
    """
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps({"image": im_b64, "email": email,"encryppass":encryppass})
    response=requests.post(url,data=payload,headers=headers)
    print(response) 

def encryption64_pass(password,n,e):
    """
        rsa 公钥加密密码
    """
    pub_key=rsa.PublicKey(n,e)
    password=password.encode('utf8')
    encrpt=rsa.encrypt(password,pub_key)

    return base64.b64encode(encrpt).decode("utf8")


if __name__ =="__main__":
    argv=sys.argv[1:]
    imagePath=""
# for demo only
    email=""
    n=0
    e=0
    password=""
    url=""
    allowd_type=('.png','.bmp','.tiff')
# ================================
#   实际使用
# -------------------------------

    try:
        opts,args=getopt.getopt(argv,"hr:m:n:e:u:p:")
    except getopt.GetoptError:
        sys.exit(2)
    if len(opts)<6:
        help()
        sys.exit()
    for opt ,arg in opts:
        if opt =='-h':
            help()
            sys.exit()
        elif opt in ('-m'):
            imagePath=arg
        elif opt in ("-n"):
            n=int(arg)
        elif opt in ('-e'):
            e=int(arg)
        elif opt in ('-u'):
            email=arg
        elif opt in ('-p'):
           password=arg
        elif opt in ('-r'):
           url=arg
           url+="upload"
        else:
           help() 
           sys.exit(2)
# ===============================================
    files=embedTool.getFilelist()
    # print(files)
    message=""
    for i in files:
            message+=i+"\n"
    
    message=trans.Str_encode(message)
    # print("messlen:{}".format(len(message)))
    # 信息需要嵌入剩余长度：
    # 分片序号
    num=0
    # 生成同一类码,同一类码为当前时间戳
    kind=time.time()
    kind=int(kind)%(1<<20)
    im_b64=None
    lsbpic="ushiwakamaru_LSB.png"
    for s in os.listdir(imagePath):
        path=os.path.join(imagePath,s)
        if os.path.isfile(path):
            filename,file_extension=os.path.splitext(path)
            if file_extension.lower() in allowd_type:
                # 获得容量
                cap=embedTool.imagecapacity(path)
                # 表示可以嵌入
                if len(message)>0 and cap > 56:
                    print("imbed Pic:"+path)
                    # 构造嵌入序列
                    imbed=""
                    imbed+=symbol
                    # 本次嵌入长度字段
                    print("cap:{}".format(cap))
                    lenght=min(cap-56,len(message))
                    print("lenght this time:{}".format(lenght))
                    imbed+=bin(lenght)[2:].zfill(20)
                    # 序号
                    imbed+=bin(num)[2:].zfill(8)
                    num+=1
                    # 同一类码
                    imbed+=bin(kind)[2:].zfill(20)
                    imbed+=message[0:lenght]
                    message=message[lenght:]
                    # 嵌入构造的信息
                    embedTool.embed(imbed,path)  
                    im_64=image_to_64b(lsbpic)
                else :
                    im_64=image_to_64b(path)
                encryp64=encryption64_pass(password,n,e)
                print("uploading....")
                send_json(url,email,encryp64,im_64)
                print("upload {} success.".format(filename+file_extension))
                time.sleep(0.5) 
                #  销毁临时文件
                if os.path.exists(lsbpic):
                    os.remove(lsbpic)
