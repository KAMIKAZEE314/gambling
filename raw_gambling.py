import os

num2symbol = {
    "0": "L",
    "1": "C",
    "2": "K",
    "3": "B",
    "4": "D",
    "5": "T",
    "6": "7"
}

def spin():
    roll = []
    for row in range(3):
        roll.append([])
        for column in range(5):
            roll[-1].append(str(int(os.urandom(1)) % 7))
    return (roll, 0)

res = spin()

# res ausgeben
roll, value = res
for row in roll:
    for column in row:
        print(column, end=" ")
    print()
    
print(value)