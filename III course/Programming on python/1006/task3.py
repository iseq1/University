def func(list,a,b,s):
    l2 = list
    if b>len(list):
        b = len(list)
    if a<0 and (len(list) + a)<0:
        a = 0
    if b < 0:
        b = len(list) + b
        if a > b:
            a, b = b - 1, a - 1
    if a < 0:
        a = len(list) + a
        if a > b:
            a, b = b - 1, a - 1
    # if s < 0:
    #     l2.reverse()
    #     s*=-1
    start = a
    finish = b
    step = s
    print(start,finish,step)
    M=[list[i] for i in range(start,finish,step)]
    return M

list = [1,2,3,4,5]
#       0 1 2 3 4
#       -5-4-3-2-1
a, b, s = 4,1,-2
print(func(list,a,b,s))