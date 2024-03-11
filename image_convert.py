from PIL import Image
import numpy
import sys


addr_to_pic = "firstgrey.webp"
image = Image.open(addr_to_pic)
bw = image.convert(mode="L")


pixels = list(bw.getdata())
width, height = bw.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
orig = sys.stdout

sys.stdout = open("fname" , 'w')
print(f"{height},{width}")

for i in range(height):
    for j in range(width):
        print(f"{pixels[i][j]}",end=",")
    print()
sys.stdout = orig
print("jobdone")

