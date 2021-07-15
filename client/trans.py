import re
def Str_encode(s:str,rule='utf-8'):
    '''
    将明文字符串按照rule的格式转化为01字符串
    :param s: 待编码字符串
    :param rule: 编码方案 默认utf-8
    :return: 字符串对应01字符串
    '''
    sc=s.encode(rule)
    bc=[bin(int(i))[2:].rjust(8,'0') for i in sc ]
    rtn=''.join(bc)
    return rtn

def Str_decode(s:str,rule='utf-8'):
    '''
    将01字符串（不加任何标识符和纠错码）转化为对应的明文字符串（默认UTF-8)
    :param s:01字符串
    :return:解码原文
    '''
    if len(s)==0:
        return '>>内容为空<<'
    if len(s)%8!=0:
        raise SyntaxError('编码不是八的倍数')
        #至少是字节的倍数才能操作
    msg=re.sub(r'0x','',hex(int(s,2)))
    rtn=bytes.fromhex(msg).decode(rule)
    return rtn

if __name__=="__main__":
    print("输入要转换的字符串：")
    message=input()
    bit=Str_encode(message)
    print(bit)
    res = Str_decode(bit)
    print(re)
