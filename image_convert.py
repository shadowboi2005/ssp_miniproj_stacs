from PIL import Image
import numpy
import sys
from math import pow,sqrt,acos,pi
import matplotlib.pyplot as plt
import cv2
import csv

constl = 'hydra'
stararr = list()
Aroi = 11
Ithresh =5
angdev = 0.1 #change in angle allowed for constellation detection

number = sys.argv[1]

addr_to_pic = "./sm_imgs/"+constl+"/image_"+str(number)+".png"
image = Image.open(addr_to_pic)
bw = image.convert(mode="L")

#getting brightness data
pixels = list(bw.getdata())
width, height = bw.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
orig = sys.stdout
pixels = numpy.array(pixels)
numpy.pad(pixels,pad_width=Aroi,mode='constant',constant_values=0)

#define datatype starstars
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

def centroid():
    offset = int((Aroi-1)/2)
    for i in range(offset,height-offset):
        for j in range(offset, width - offset):
            if pixels[i][j] > Ithresh:
                temp = [pixels[k][j-offset : j+offset+1] for k in range(i-offset,i+offset+1)]
                #print(f"{len(temp)} at {i} , {j} with brightness {temp[offset][offset]}")
                xtemp= 0 
                ytemp = 0
                btemp = 0
                b2temp = 0
                for m in range(0,Aroi):
                    for n in range(0,Aroi):
                        xtemp +=  (i-offset+m)*temp[m][n]*temp[m][n]
                        ytemp += (j - offset + n)*temp[m][n]*temp[m][n]
                        btemp += temp[m][n]
                        b2temp += temp[m][n]*temp[m][n]
                xtemp = xtemp/b2temp
                ytemp = ytemp/b2temp
                btemp = btemp/(Aroi * Aroi)
                stemp = star(ytemp-Aroi,xtemp-Aroi,btemp)
                #print(f"{stemp} , {i} , {j} ")

                flag = 0
                for star1 in stararr:
                    if stemp.dist(star1) < Aroi:
                        star1.x = star1.x*star1.b*star1.b*star1.n + stemp.x*stemp.b*stemp.b
                        star1.y = star1.y*star1.b*star1.b*star1.n + stemp.y*stemp.b*stemp.b
                        star1.x /= star1.b*star1.b*star1.n + stemp.b*stemp.b
                        star1.y /= star1.b*star1.b*star1.n + stemp.b*stemp.b
                        star1.b = star1.b*star1.n + stemp.b
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

stararr.sort(key=lambda i: i.b , reverse=True)

with open(constl+'.csv', 'w',newline="") as csvfile1:
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
cv2.imwrite("img11_new.jpg",image)



#constellation detection


constln = {'canismajor':0,'orion':0,'hydra':0,'puppis':0,'perseus':0}
anglerep = list()
with open('trial.csv', 'r',newline="") as csvfile1:
    reader = csv.reader(csvfile1)
    for row in reader:
        anglerep.append([float(row[0]),float(row[1]),float(row[2]),"hydra"])
    csvfile1.close()

def angles(star1,star2,star3):
    a = star1.dist(star2)
    b = star2.dist(star3)
    c = star3.dist(star1)
    A = (a*a + c*c - b*b)/(2*a*c)
    B = (a*a + b*b - c*c)/(2*a*b)
    C = (b*b + c*c - a*a)/(2*b*c)
    A= 180*acos(A)/pi
    B= 180*acos(B)/pi
    C= 180*acos(C)/pi
    return [A,B,C]

for i in stararr:
    for j in stararr:   
        for k in stararr:
            if i!=j and j!=k and i!=k:
                for ang in anglerep:
                    angmes = angles(i,j,k)
                    if (abs(ang[0] - angmes[0]) < angdev)and (abs(ang[1] - angmes[1]) < angdev) and (abs(ang[2] - angmes[2]) < angdev):
                        constln[ang[3]] += 1    
                    
max_key = max(constln, key=constln.get)
if constln[max_key] > 0:
    print("constellation detected", max_key, "with", constln[max_key], "triangles spotted")
else:
    print("no constellation detected")

