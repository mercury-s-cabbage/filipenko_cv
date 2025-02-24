f = open("responses.txt")
real = []
pred = []
for line in f:
    line = line.split()
    if line[0] == "positive":
        real.append(1)
    else:
        real.append(0)
    if line[1] == "positive":
        pred.append(1)
    else:
        pred.append(0)

TPTN = 0
for i in range(len(real)):
    if real[i] == pred[i]:
        TPTN += 1

print("Accuracy = ", TPTN/len(real))

T2 = 0
T1 = 0
for i in range(len(real)):
    if real[i] == 1:
        T1 += 1
        if pred[i] == 1:
            T2 += 1

print("Recall = ", T2/T1)

