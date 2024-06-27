l = [1,2,3,4,5,6]
print(all(l[i]>0 for i in range(len(l)) if i%2==0))
print(all(item>0 for item in l[::2]))