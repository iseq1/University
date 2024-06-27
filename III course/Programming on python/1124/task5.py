l = [1,2,9]

def average(lst):
    if len(lst) == 0:
        return None
    else:
        return sum(lst)/len(lst)

if(average(l) == None):
    print('была передана коллекция нулевой длины')
else:
    print(average(l))