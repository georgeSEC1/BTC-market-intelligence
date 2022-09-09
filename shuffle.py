import random
with open("test.csv", encoding='ISO-8859-1') as f:
    text = f.readlines()
lines = text
random.shuffle(lines)
f = open("testB.csv", "a", encoding="utf8")
for line in lines:
    f.write(line)