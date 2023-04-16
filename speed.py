import cv2
import math
import os
import inread
import output


def dis(a, b):
    return math.sqrt(a * a + b * b)

def draw_speed(cur,pre,tim,sta):
    prex = pre[0][0]
    curx= cur[0][0]
    cury= cur[1][0]
    num = "Speed: 0 m/s"
    if (curx[8] and prex[8]):
    #8号到一号的像素距等价于0.55m
        if (sta==-1 or math.fabs(sta-dis(curx[8] - curx[1], cury[8] - cury[1]))<2):
            sta = dis(curx[8] - curx[1], cury[8] - cury[1])
        num=round(math.fabs( (curx[8]-prex[8]) /sta*0.55/(1/24*tim)),2)
        num="Speed: "+str(num)+" m/s"
    return num,sta

#inread.start()

lis1 = os.listdir("./data/json")
lis2 = os.listdir("./data/image")
i = 0
sta=-1
num="Speed: 0 m/s"
id=0
prex=-1
while (i < len(lis1)):
    lis = inread.readjson(lis1[i])
    img = cv2.imread('./data/image/' + lis2[i])
    ret = output.draw(lis, img,img.shape)

    if (prex==-1) :
        prex=lis[0][0][8]
        id=i
    else:
        if (lis[0] and math.fabs(prex-lis[0][0][8])>10):
            pre = inread.readjson(lis1[id])
            num,sta=draw_speed(lis,pre,i-id,sta)
            id=i
            prex=lis[0][0][8]
    mi=min(img.shape[0],img.shape[1])
    cv2.putText(ret, str(num), (ret.shape[1]//2-80 , 30), cv2.FONT_HERSHEY_PLAIN, 1.7*mi//500, (0, 0,250), 2)
    tmp = str(i)
    while (len(tmp) < 3):
        tmp = "0" + tmp
    i += 1
    cv2.imwrite("data/ret/" + 'ret' + tmp + '.jpg', ret)

output.outvedio()
#output.clean()