# coding:utf8
import win32api, win32con, win32gui
import re, os, sys, argparse
from PIL import Image,ImageFont,ImageDraw
import requests
from bs4 import BeautifulSoup
import urllib.request,random,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
url='http://wufazhuce.com/one/'
root = 'D:\\zx'

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
    dir = root + '\\素材\\'+str(i)+'.jpg'
    f = open(dir, "wb")
    f.write(data)
    f.close()
    return dir

#屏幕分辨率
pixel = (1920, 1200)
#屏幕背景颜色
backcolor = (0,0,0)
#文字样式
color = 'yellow'
board = (pixel[0]//2,pixel[1]//2)
font = ImageFont.truetype('simsun.ttc', 25)

def drawText(dir,text):
    newImg = Image.new("RGBA", pixel, backcolor)
    img = Image.open(dir)
    w,h = img.size
    y_s = 550
    x_s = w * y_s //h
    img = img.resize((x_s, y_s), Image.ANTIALIAS)
    loc = ((pixel[0]-x_s)//2,(pixel[1]-y_s)//4)
    newImg.paste(img,loc)
    draw = ImageDraw.Draw(newImg)
    board = (loc[0]+100,loc[1]+y_s+50)
    draw.text(board, text, color, font=font)
    return newImg

def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


def set_wallpaper(img):
    # # 把图片格式统一转换成bmp格式,并放在源图片的同一目录
    # img_dir = os.path.dirname(img_path)
    # bmpImage = Image.open(img_path)
    # new_bmp_path = os.path.join(img_dir, 'wallpaper.bmp')
    new_bmp_path = root + '\当前背景.bmp'
    img.save(new_bmp_path, "BMP")
    set_wallpaper_from_bmp(new_bmp_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no', default=0, type=int, help='VOL NO, val 0 indicates random')
    parser.add_argument('--show', default=0, type=int, help='show words today')
    args = parser.parse_args()

    if (args.show != 0):
        i = getNewIndex()
    else:
        if (args.no == 0):
            i = random.randint(14, int(getNewIndex()))
        else:
            i = args.no

    # if (len(sys.argv) != 1):
    #     i = sys.argv[1]
    # else:
    #     i = random.randint(14,no)
    print('index:',i)
    text = oneCita(i)
    path,image = oneImagen(i)
    dir = path
    newImg = drawText(dir,text)
    # newImg.show()
    set_wallpaper(newImg)
    newImg.save(root + '\\背景\\bg'+str(i)+'.bmp')

if __name__ == '__main__':
    if(not os.path.exists(root + '\\素材')):
        os.makedirs(root + '\\素材')
    if (not os.path.exists(root + '\\背景')):
        os.makedirs(root + '\\背景')
    main()