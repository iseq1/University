list = [1,5,8,9,123,6234,347,3,5436,1029]

print("Sorted list:")
for i in range(len(list)-1):
    for j in range(len(list)-i-1):
        if list[j] > list[j+1]:
            list[j], list[j+1] = list[j+1], list[j]
print(list)


print("Reversed list:")
lastindex = len(list)-1
for i in range(0, len(list)//2):
    list[i], list[lastindex] = list[lastindex], list[i]
    lastindex+=-1
print(list)

list.append("a")
list.append("b")
list.append("c")
list.append("d")
print("New list")

#найти в списке все числа, которые больше числа M, приэтом использовать isinstance

# Пример использования
M = 12
result = [x for x in list if isinstance(x, int) and x > M]
print(list)
print("Number of elements in the list that are greater than M =",M,": ",len(result))