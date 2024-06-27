def check_speeding(v_max, segments):
    total_distance = 0
    total_time = 0

    for v, t in segments:
        total_distance += v * t
        total_time += t

    average_speed = total_distance / total_time

    if average_speed > v_max:
        return 1
    else:
        return 0


line = input().split()
N, V_max = int(line[0]), int(line[1])
segments = []
for i in range(N):
    newline = input().split()
    segments.append((int(newline[0]), int(newline[1])))
print(check_speeding(V_max, segments))