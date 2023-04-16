import cv2
import os
import inread
import output
import math

Pi = math.acos(-1)
def dis(a, b):
    return math.sqrt(a * a + b * b)

def calc(x, y, j, i, k):
    if (x[i] == 0 or x[j] == 0 or x[k] == 0): return -1
    p1x = x[j] - x[i]
    p2x = x[k] - x[i]
    p1y = y[j] - y[i]
    p2y = y[k] - y[i]
    if (dis(p1x, p1y) * dis(p2x, p2y)==0): return -1
    num = round(math.acos((p1x * p2x + p1y * p2y) / (dis(p1x, p1y) * dis(p2x, p2y))) / Pi * 180.0, 1)
    return num

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y


#inread.start()

lis1 = os.listdir("./data/json")
lis2 = os.listdir("./data/image")
sta = -1 #输入处理比例尺

lisa=[] #前一帧是锐角，后一帧是钝角
lax=[]
lay=[]
la=[]
for i in range(1,len(lis1)): #脚踝为钝角的帧
    lis = inread.readjson(lis1[i])
    if (lis[0]):

        curx=lis[0][0]
        cury=lis[1][0]

        lx=calc(curx, cury, 9, 10, 11)
        lh=calc(curx, cury, 10, 11, 22)
        rx=calc(curx, cury, 12, 13, 14)
        rh=calc(curx, cury, 13, 14, 19)
        if (lx>145 and lh>120 and rx<145 and rh<120):
            lisa.append((i,22))
            lax.append(curx[22])
            lay.append(cury[22])
            la.append(dis(curx[8] - curx[1], cury[8] - cury[1]))

        if (rx>145 and rh>120 and lx<145 and lh<120):
            lisa.append((i,19))
            lax.append(curx[19])
            lay.append(cury[19])
            la.append(dis(curx[8] - curx[1], cury[8] - cury[1]))

lise=[lisa[0]]
lisx=[lax[0]]
lisy=[lay[0]]

for i in range(0,len(lisa)):
    siz=len(lise)-1


    if (i>0 and (lisa[i][1]!=lise[siz][1]) and lisa[i][0]!=lise[siz][0]+1 ): #左右脚不等且帧不连 在地面
        sta=la[i]
        cdis=dis(lax[i]-lisx[siz],lay[i]-lisy[siz])/sta*0.55

        if ( cdis>0.5 and cdis<3): #前一帧到这一帧距离大于0.5m
            lise.append(lisa[i])
            lisx.append(lax[i])
            lisy.append(lay[i])

lisd=[]
lista=[]
siz=0
i=0
while (i < len(lis1)):  #读取每个张图片,返回ret图片
    lis = inread.readjson(lis1[i])
    img = cv2.imread('./data/image/' + lis2[i])
    ret=output.draw(lis,img,img.shape)
    if (lis[0]):
        curx=lis[0][0]
        cury=lis[1][0]
        if (siz<len(lise) and i>=lise[siz][0]):
            id=lise[siz][1]
            lisd.append(Point(curx[id],cury[id]))
            siz+=1
            lista.append(dis(curx[8] - curx[1], cury[8] - cury[1]))
    mi=min(img.shape[0],img.shape[1])
    if (len(lisd)>1):
        for j in range(0,len(lisd)-1):
            x1=lisd[j].x
            x2=lisd[j+1].x
            y1=lisd[j].y
            y2=lisd[j+1].y
            cv2.line(ret,(x1,y1), (x2,y2),(0,255,0),3)
            sta=lista[j]
            num=round(dis(x1-x2,y1-y2)/sta*0.55,2)

            cv2.circle(ret, (x2, y2), 10, (255,0,0), -1)

            cv2.putText(ret, str(num)+"m", ((x1+x2)// 2 , (y1+y2)//2), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.6*mi//500, (255, 0, 0),1)

    tmp=str(i)
    while (len(tmp)<3):
        tmp="0"+tmp
    i += 1
    cv2.imwrite("data/ret/" + 'ret' + tmp + '.jpg', ret)


output.outvedio()
#output.clean()