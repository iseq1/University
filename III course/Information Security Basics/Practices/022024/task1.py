import math
from datetime import datetime, date, time
def GCD(a, b):
    start_time = datetime.now()
    count = 0
    while b:
        a, b = b, a%b
        count+=1
    end_time = datetime.now()
    time_diff = end_time - start_time
    return (a, count, time_diff.microseconds)

print(f'My function: {GCD(10946, 17711)}\nMath function: {math.gcd(210, 45)}')

