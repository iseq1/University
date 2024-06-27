n = int(input("Give count of number "))
list = [int(input("Give a number ")) for i in range(n)]

currentMin = 1231241234
Min = currentMin
currentMax = -1231245123
Max = currentMax
Average = 0
currentLen = 0
MaxLen = 0
posititv = True
increase = True
for i in range(len(list)):
    #1
    if list[i] < currentMin:
        currentMin = list[i]
        if currentMin<Min:
            Min=currentMin

    if list[i] > currentMax:
        currentMax = list[i]
        if currentMax>Max:
            Max=currentMax

    Average += list[i]
    #2
    if list[i]<0:
        posititv = False
    #3
    if i<len(list)-1:
        if list[i]>list[i+1]:
            increase=False
        if list[i] < list[i + 1]:
            currentLen += 1
            if currentLen > MaxLen:
                MaxLen = currentLen
        else:
            currentLen = 1




print("\nMax = ",Max, "\nMin = ", Min, "\nAverage = ", Average/len(list))

if increase:
    if posititv:
        print("There is not symbol under 0")
    else:
        print("There is symbol under 0")
    print("Numbers in increasing order")
else:
    print("Numbers are not in increasing order")

#5
print("the longest ascending sequence: ",MaxLen)

#6
currentMLTP = 0
maxMLTP = 0
for i in range(len(list)):
    for j in range(i,len(list)):
        if list[i]*list[j] > maxMLTP and i!=j:
            maxMLTP = list[i]*list[j]
            answer = (list[i],list[j])
print("Pair with the largest product of numbers: ", answer, " - ",maxMLTP)

#4
diff = True
difference = list[1] - list[0]
for i in range(2, len(list)):
    if list[i] - list[i-1] != difference:
        diff = False
        exit()
if diff:
    print("numbers in progression")
else:
    print("numbers are not in progression")

