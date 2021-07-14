import os
import rsa
import time
import sys,getopt
import base64
import json
import requests
import glob
import embed

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
    imagePath="img"
    email="demo@qq.com"
    n=10873683812093980312876261455931339154868839297911186360501106374970623887498974469508709631928262264176897078718325920450250100152077649157386005292445697
    e=65537
    password="demo"
    url="http://192.168.43.137:5000/upload"
    allowd_type=('.png','.bmp','.tiff')
# ================================
#   实际使用
# -------------------------------
#    try:
#        opts,args=getopt.getopt(argv,"hm:n:e:u:p:")
#    except getopt.GetoptError:
#        help()
#        sys.exit(2)
#    for opt ,arg in opts:
#        if opt =='-h':
#            help()
#            sys.exit()
#        elif opt in ('-m'):
#            imagePath=arg
#        elif opt in ("-n"):
#            n=int(arg)
#        elif opt in ('-e'):
#            e=int(arg)
#        elif opt in ('-u'):
#            email=arg
#        elif opt in ('-p'):
#           password=arg
#        elif opt in ('-r'):
#           url=arg
#        else:
#           help() 
#           sys.exit(2)
# ===============================================
    lsbpic="ushiwakamaru_LSB.png"
    for s in os.listdir(imagePath):
        path=os.path.join(imagePath,s)
        if os.path.isfile(path):
            filename,file_extension=os.path.splitext(path)
            if file_extension.lower() in allowd_type:
                embed.embed(path) # 隐私信息嵌入
                im_64=image_to_64b(lsbpic)
                encryp64=encryption64_pass(password,n,e)
                print("sending....")
                send_json(url,email,encryp64,im_64)
                print("upload {} success.".format(filename+file_extension))
                time.sleep(0.5) # 每隔两秒发一次
