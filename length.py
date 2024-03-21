import math
import csv


def calculate_length(x1, y1, x2, y2):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


'''
with open('./hydra.csv','r',newline="") as csvfile1:
    reader = csv.reader(csvfile1)
    writer = csv.writer(open("./constls/hydra_l",'w',newline=""))
    for k in reader:
        line_length = [calculate_length(k[0], k[1], k[2], k[3]),calculate_length(k[2], k[3], k[4], k[5]),calculate_length(k[4], k[5], k[0], k[1])]
        print("The length of the line is:", line_length)
        writer.writerow(line_length)
print("done")
'''