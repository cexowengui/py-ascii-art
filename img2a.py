"""
img2a.py

A python program that convert images to ASCII art.

Author: angus hsiung
"""

import sys, random, argparse
import numpy as np
import math

from PIL import Image

# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/
# 10 levels of gray
gscale = '@%#n+=-;. '


def getAverageL(image):
    """
    得到图像的灰度平均值
    """
    im = np.array(image)
    # get shape
    w, h = im.shape

    # average reshape()得到一个一维矩阵
    # get average
    return np.average(im.reshape(w * h))


def convertImgToAsciiTxt(filename, cols, scale):
    '''
    输入一个图像文件，返回一个txt str
    :param filename: 图像名
    :param cols: txt的列
    :param scale: 一个字符的长宽比，0.43适合宋体或者Courier font，计算小格的垂直分辨率
    :return: asciiImg
    '''
    global gscale
    #得到一个灰度图
    img = Image.open(filename).convert('L')
    #get dims
    W, H = img.size[0], img.size[1]
    #w 是每个小格的水平分辨率
    w = W/cols
    #h是小格的垂直分辨率
    h = w/scale
    #图片垂直分辨率/小格垂直分辨率=字符的行数
    rows = int(H/h)
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims(w*h): %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)


    #txt store the string
    txt = []
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        if j == rows-1:
            y2 = H
        #append a " " in the end of a line
        txt.append("")
        for i in range(cols):
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            # correct last tile
            if i == cols-1:
                x2 = W
            #get a lattice image use the x1 x2 y1 y2
            lattice = img.crop((x1,y1,x2,y2))
            #get the average
            avg = int(getAverageL(lattice))

            #get the suit charactor from gscale using avg

            graychar = gscale[int((avg*9)/255)]

            #append the char to the txt string
            txt[j] +=graychar

    return txt


#main function
def main():
    # create parser
    descriptionStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descriptionStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols',dest='cols',required=False)
    # parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    outFile = "out.txt"
    if args.outFile:
        outFile = args.outFile

    cols = 100
    if args.cols:
        cols = int(args.cols)

    txt = convertImgToAsciiTxt(imgFile,cols,scale)

    #write the txt to the file
    f = open(outFile, 'w')
    for row in txt:
        f.write(row + '\n')

    #close the file
    f.close()
    print("ASCII art write to: " + outFile)


# call main
if __name__ == '__main__':
    main()
