from PIL import Image
import numpy
import sys
from math import pow,sqrt
import matplotlib.pyplot as plt
import cv2
import csv


addr_to_pic = "images/image_2.jpg"
image = Image.open(addr_to_pic)
bw = image.convert(mode="L")

#getting brightness data
pixels = list(bw.getdata())
width, height = bw.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
orig = sys.stdout

#define datatype star
class star:
    def __init__(self,x,y,b):
        self.x = x
        self.y = y
        self.b = b
        self.n = 1
    def __str__(self):
        return f"(x = {self.x},y = {self.y},b = {self.b})"
    def dist(self, star2):
        return sqrt(pow(self.x-star2.x , 2) + pow(self.y - star2.y , 2))
    


#the list that is going to hold the stars
stararr = list()
Aroi = 11
Ithresh = 3

def centroid():
    offset = int((Aroi-1)/2)
    for i in range(offset,height-offset):
        for j in range(offset, width - offset):
            if pixels[i][j] > Ithresh:
                temp = [pixels[k][j-offset : j+offset+1] for k in range(i-offset,i+offset+1)]
                #print(f"{len(temp)} at {i} , {j} with brightness {temp[offset][offset]}")
                '''
                Ibound = 0
                for k in range(0,Aroi):
                    Ibound += (temp[0][k] + temp[k][0]+temp[Aroi-1][k]+ temp[k][Aroi-1])
                Ibound -= (temp[0][0]+ temp[Aroi-1][0] + temp[Aroi-1][Aroi-1] + temp[0][Aroi -1])
                Ibound /= (4*(Aroi-1))
                for m in range(0,Aroi):
                    for n in range(0,Aroi):
                        temp[m][n] -= Ibound
                '''
                xtemp= 0 
                ytemp = 0
                btemp = 0
                for m in range(0,Aroi):
                    for n in range(0,Aroi):
                        xtemp +=  (i-offset+m)*temp[m][n]
                        ytemp += (j - offset + n)*temp[m][n]
                        btemp += temp[m][n]
                xtemp = xtemp/btemp
                ytemp = ytemp/btemp
                btemp = btemp/(Aroi * Aroi)
                stemp = star(ytemp,xtemp,btemp)
                #print(f"{stemp} , {i} , {j} ")

                flag = 0
                for star1 in stararr:
                    if stemp.dist(star1) < Aroi:
                        star1.x = star1.x*star1.b*star1.n + stemp.x*stemp.b
                        star1.y = star1.y*star1.b *star1.n + stemp.y*stemp.b
                        star1.b = star1.b*star1.n + stemp.b
                        star1.x /= star1.b
                        star1.y /= star1.b
                        star1.b /= 1+star1.n
                        flag = 1
                        star1.n += 1
                        break
                if flag ==0:
                    stararr.append(stemp)



centroid()
print(len(stararr))
ax = []
ay = []
size = []
for i in stararr:
    #print(i)
    ax.append(i.x)
    ay.append(height - i.y)
    size.append(i.b)

with open('img2.csv', 'w',newline="") as csvfile1:
    writer = csv.writer(csvfile1)
    writer.writerow(['x coord' , 'y coord' , 'brightness'])
    for i in stararr:
        writer.writerow([f'{i.x + 1}' , f'{i.y+1}',f'{i.b}'])
    csvfile1.close()



#plotting the graph    
fig, axis = plt.subplots()
axis.scatter(ax,ay,s = size)
axis.set(xlim = (0,width) , ylim = (0,height))
plt.show()

#sending image to a file
sys.stdout = open("fname" , 'w')
print(f"{height},{width}",end=",")

for i in range(height):
    for j in range(width):
        print(f"{pixels[i][j]}",end=",")
    print()
sys.stdout = orig
print("jobdone")

image = cv2.imread(addr_to_pic)
window_name = 'image'

#drawing the circles
for i in stararr:
    center_coord = (round(i.x),round(i.y))
    rad = int((Aroi+1)/2)
    color = (255,0,0)
    thickness = 2
    image = cv2.circle(image, center_coord,rad,color,thickness)
cv2.imwrite("image_2_new_circled.jpg",image)

