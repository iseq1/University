def func(list):
    a = [b for b in list if b>0]
    return len(a)==len(list)

list = [1,2,3]
print(func(list))