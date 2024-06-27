l = [1,2,3,7,11,13,17]
def IsPrime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n

def simple(l):
    if all(IsPrime(item) for item in l):
        return 'Y'
    else:
        return 'N'

print(simple(l))