import math
import csv

def calculate_angles(a, b, c):
    # Calculate the angles using the Law of Cosines
    a = float(a)
    b = float(b)
    c = float(c)
    angle_A = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
    angle_B = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
    angle_C = 180 - angle_A - angle_B

    return angle_A, angle_B, angle_C

constl = 'orion'

k = []
with open('./constls/'+constl+'_triangles_len', 'r', newline='') as csvfile1:
    reader = csv.reader(csvfile1)
    for row in reader:
        k.append(sorted(calculate_angles(row[0], row[1], row[2])))
    csvfile1.close()

with open('anglerep.csv','+a',newline="") as csvfile1:
    writer = csv.writer(csvfile1)
    for i in k:
        writer.writerow(i)
    csvfile1.close()

print(k)
