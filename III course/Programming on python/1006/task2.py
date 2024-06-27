def func(list):
    a = [b for b in list if b%2==0]
    return len(a)>=1

list = [1,2,3]
print(func(list))