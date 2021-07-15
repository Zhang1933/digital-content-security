def crawler(url = 'http://192.168.43.137:5000/',store_path = 'images\\'):

    from os import fspath
    import re
    from urllib.request import HTTPDigestAuthHandler
    import requests
    import time
    #初始化访问页
    first_page = 1

    #判断是否翻页
    PageNext = 1
    store = []
    while PageNext == 1:
    
        time.sleep(3)
        str_of_Page = str(first_page)
        url_im = url + 'index/?page=' + str_of_Page
        html = requests.get(url = url_im).text
        img_url = re.findall('src="(.*?)" class=',html,re.S)
        store += img_url
    
        if('next page' in html):
            PageNext = 1
            first_page += 1
         
        else:
            PageNext = 0
        #正则表达式筛选所有图片
    
    i = 0

    for each in store:
        time.sleep(3)
        print(each)
        #打印抓取图片的路径
        try:
            img = requests.get(url+each,timeout=10)
        except requests.exceptions.ConnectionError:
            print('error: can not download this image')
            continue
        #保存图片
        string = store_path + str(i) + '.png'
        fp = open(string,'wb')
        fp.write(img.content)
        fp.close()
        i += 1
