import cv2
import os

def outvedio():
    path = "./data/ret/"
    filelist = os.listdir(path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  #opencv版本是3

    fps = 24  # 视频每秒24帧
    tmp = cv2.imread("./data/ret/"+filelist[0])
    size = tmp.shape # 需要转为视频的图片的尺寸

    video = cv2.VideoWriter("video.mp4", fourcc, fps, (size[1],size[0])) # 视频保存在当前目录下

    for item in filelist:
        item = path + item
        img = cv2.imread(item)
        video.write(img)
    video.release()
    cv2.destroyAllWindows()
def clean():
    os.system("del data\image\*.png")
    os.system("del data\\ret\*.jpg")
    os.system("del data\json\*.json")

#在原图上划线盖住openpose 打水印
def draw(a,ret,siz):

    def drawline(x, y, p, q):
        if (x[p] and y[p] and x[q] and y[q]):
            cv2.line(ret, (x[p], y[p]), (x[q], y[q]), (0, 255, 255), 4) #分别表示B G R

    i=0
    while (i<len(a[0])):
        xlis=a[0][i]
        ylis=a[1][i]
        drawline(xlis,ylis, 0, 1)
        drawline(xlis,ylis, 1, 2)
        drawline(xlis,ylis, 2, 3)
        drawline(xlis,ylis, 3, 4)
        drawline(xlis,ylis, 1, 8)
        drawline(xlis,ylis, 8, 9)
        drawline(xlis,ylis, 9, 10)
        drawline(xlis,ylis, 10, 11)
        drawline(xlis,ylis, 8, 12)
        drawline(xlis,ylis, 12, 13)
        drawline(xlis,ylis, 13, 14)
        drawline(xlis,ylis, 1, 5)
        drawline(xlis,ylis, 5, 6)
        drawline(xlis,ylis, 6, 7)
        drawline(xlis,ylis, 0, 15)
        drawline(xlis,ylis, 15, 17)
        drawline(xlis,ylis, 0, 16)
        drawline(xlis,ylis, 16, 18)
        drawline(xlis,ylis, 11, 22)
        drawline(xlis,ylis, 14, 19)
        drawline(xlis,ylis, 11, 24)
        drawline(xlis,ylis, 23, 22)
        drawline(xlis,ylis, 14, 21)
        drawline(xlis,ylis, 19, 20)
        i=i+1

    biglogo = ret - ret
    ls=min(siz[0],siz[1])//10

    logo = cv2.imread("./data/logo.jpg")
    logo = cv2.resize(logo,(ls,ls),fx=1,fy=1,interpolation=cv2.INTER_CUBIC)
    xq=0
    yq=ret.shape[1]-logo.shape[1]-10
    biglogo[xq : xq + logo.shape[0], yq : yq+logo.shape[1]] = logo
    ret = cv2.addWeighted(ret, 1, biglogo, 1,1)
    ret=cv2.putText(ret, "Loop Burn", (ret.shape[1]-100*ls//50 , ret.shape[0]-20), cv2.FONT_HERSHEY_PLAIN, ls//50, (255, 255, 0),2*ls//50)
    return ret