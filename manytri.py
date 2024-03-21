import length
import csv
import angle

x= []
with open('./hydra.csv','r',newline="") as csvfile1:
    reader = csv.reader(csvfile1)
    for k in reader:
        x.append((k[0],k[1]))
lst = []
for i in x:
    for j in x:
        for k in x:
            if i != j and j != k and k != i:
                p = (length.calculate_length(i[0],i[1],j[0],j[1]),length.calculate_length(j[0],j[1],k[0],k[1]),length.calculate_length(k[0],k[1],i[0],i[1]))
                j = sorted(angle.calculate_angles(p[0],p[1],p[2]))
                if j not in lst:
                    lst.append(j)
writer = csv.writer(open("trial.csv",'w',newline=""))
for i in lst:
    writer.writerow(i)
