# coding:utf8
from PIL import Image
import win32api, win32con, win32gui
import re, os, sys, argparse
from drawText import *

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
    new_bmp_path = 'wallpaper.bmp'
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
    dir = os.getcwd() + '\\' +path
    newImg = drawText(dir,text)
    # newImg.show()
    set_wallpaper(newImg)
    newImg.save('background/bg'+str(i)+'.jpg')

if __name__ == '__main__':
    main()