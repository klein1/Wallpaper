# coding:utf8
import requests
from bs4 import BeautifulSoup
import urllib.request,random,re,sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
url='http://wufazhuce.com/one/'
i = 1356

def random_space():
    num = random.randint(3,10)
    return ' '*num

def getNewIndex():
    website = 'http://www.wufazhuce.com'
    no = 0
    try:
        res = requests.get(website)
        res.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        index = soup.find_all('a')[1]['href']
        no = index[index.rfind('/')+1:]
        print('new number:\n',no)
    return no

def oneCita(i):
    content = ''
    currenturl = url + str(i)
    try:
        res = requests.get(currenturl)
        res.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.select('.one-cita')
        text = text[0].string.strip()

        text = re.split('[，。]',text)
        for i in range(len(text)):
            content += text[i]+'\n'
        content = content[0:-1]

        # text = ' '*10+text
        # text = text.replace('，','，\n'+random_space()).replace('。','。\n'+random_space())
        print('content:\n',content)
    return content

def oneImagen(i):
    path = ''
    image = ''
    currenturl = url + str(i)
    try:
        res = requests.get(currenturl)
        res.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find_all('img')[1]
        image = image['src']
        print('image:\n',image)
        path = downloadImg(i,image)
        print('download image:\n', path)
    return path,image

def downloadImg(i,url):
    web = urllib.request.urlopen(url)
    data = web.read()
    dir = 'one_img\\'+str(i)+'.jpg'
    f = open(dir, "wb")
    f.write(data)
    f.close()
    return dir

if __name__ == '__main__':
    # oneCita(i)
    getNewIndex()