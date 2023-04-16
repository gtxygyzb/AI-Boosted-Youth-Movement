import cv2
import math
import os
import inread
import output

global mi

Pi = math.acos(-1)
def dis(a, b):
    return math.sqrt(a * a + b * b)

def calc(x, y, j, i, k ,ret,id):
    if (x[i] == 0 or x[j] == 0 or x[k] == 0): return 0
    p1x = x[j] - x[i]
    p2x = x[k] - x[i]
    p1y = y[j] - y[i]
    p2y = y[k] - y[i]
    if ((dis(p1x, p1y) * dis(p2x, p2y))==0): return 0
    num = str(round(math.acos((p1x * p2x + p1y * p2y) / (dis(p1x, p1y) * dis(p2x, p2y))) / Pi * 180.0, 1))

    xq=20
    yq=0
    if (id==1):
        num="Left knee:"+num
        yq=25
    if (id == 2):
        num = "Left ankle:" + num
        yq=50
    if (id == 3):
        num = "Right knee:" + num
        yq=75
    if (id == 4):
        num = "Right ankle:" + num
        yq=100
    cv2.putText(ret, num, (xq, yq), cv2.FONT_HERSHEY_PLAIN,1*mi//500, (255, 0 ,255), 2)

#inread.start()

lis1 = os.listdir("./data/json")
lis2 = os.listdir("./data/image")
i = 0
while (i < len(lis1)):  #读取每个张图片,返回ret图片
    lis = inread.readjson(lis1[i])
    img = cv2.imread('./data/image/' + lis2[i])
    mi=min(img.shape[0],img.shape[1])
    ret = output.draw(lis, img ,img.shape)
    xlis = lis[0]
    ylis = lis[1]
    j = 0
    #while (j < len(xlis)):
    curx = xlis[j]
    cury = ylis[j]
    calc(curx, cury, 9, 10, 11, ret , 1)
    calc(curx, cury, 10, 11, 22, ret , 2)
    calc(curx, cury, 12, 13, 14, ret , 3)
    calc(curx, cury, 13, 14, 19, ret , 4)
     #j += 1

    tmp=str(i)
    while (len(tmp)<3):
        tmp="0"+tmp
    i += 1
    cv2.imwrite("data/ret/" + 'ret' + tmp + '.jpg', ret)

output.outvedio()
#output.clean()