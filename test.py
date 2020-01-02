k = [1]
count = 0
flag = False
for i in k:
    count += 1
    print(count)
    if not flag:
        k.append(2)
        k.append(3)
        k.append(4)
        flag = True

[print(i) for i in range(2, int(5))]