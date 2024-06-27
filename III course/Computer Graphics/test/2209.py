list = [1, 2, 3, 4, 1]
count=0
for i in list:
    if i==1:
        count+=1
print(count)

#============================#

list = [1, 2, 3, 4, 1]
max_count = 0
result = None
for i in list:
    count = 0
    for j in list:
        if j == i:
            count += 1
    if count > max_count:
        max_count = count
        result = i
print(result)

#============================#

str = "HeLlo"
str = str.lower()
max_count = 0
result = None
for i in str:
    count = 0
    for j in str:
        if j == i:
            count += 1
    if count > max_count:
        max_count = count
        result = i
print(result)

#============================#

list = [1, 2, 3, 3, 1]
result = [[]]

print(result)