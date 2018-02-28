from PIL import Image,ImageFont,ImageDraw
from oneDownload import *

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

if __name__ == '__main__':
    i = 1990
    img = Image.open('background/image2.jpg')
    text = oneCita(i)
    # path,image = oneImagen(i)
    # path = os.getcwd() + path
    # drawText(img,text).show()

