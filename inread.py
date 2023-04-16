import os
import json
import math

def dis(a, b):
    return math.sqrt(a * a + b * b)
#运行openpose导出json和有标记的图片
def start():
    path=os.getcwd()
    fl = os.listdir(path)
    for item in fl:
        if (item !='video.mp4') and (item.endswith('.mp4') or item.endswith('.avi') or item.endswith('.wmv') or item.endswith('.mkv')):
            os.system("bin\OpenPoseDemo.exe --video "+item+" --write_json data/json/ --write_images data/image/")
            break

#输入json文件名，返回( x[ 第一个人[] , 第二个人[] ],y[第一个人[] , 第二个人 []] )
def readjson(rt):
    with open("./data/json/" + rt, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    data = json_data["people"]

    retx=[]
    rety=[]
    cnt=0
    g=int(0)
    gx=[]
    gy=[]

    for item in data:
        cnt=cnt+1
        x=[]
        y=[]
        tmp=item["pose_keypoints_2d"]
        for k in range(0, 74, 3):
            x.append(int(tmp[k]))
            y.append(int(tmp[k + 1]))
        if (gx==[] or dis(x[8]-x[1],y[8]-y[1])>dis(gx[8]-gx[1],gy[8]-gy[1])) :
            gx=x
            gy=y
            g=cnt

    retx.append(gx)
    rety.append(gy)

    cnt=0
    for item in data:
        cnt+=1
        x=[]
        y=[]
        tmp=item["pose_keypoints_2d"]
        for k in range(0, 74, 3):
            x.append(int(tmp[k]))
            y.append(int(tmp[k + 1]))
        if (cnt!=g):
            retx.append(x)
            rety.append(y)
    return (retx,rety)
