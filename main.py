import sys

source = sys.argv[1]
i = 0
while i < len(source) - 1:
    if source[i].isdigit():
        if source[i + 1] == " ":
            i += 2
            while i < len(source) - 1 and source[i] == " ":
                i += 1
            if i < len(source) - 1 and source[i].isdigit():
                raise TypeError
    i += 1

source = source.replace(" ", "")
if(source[-1] == '+'  or source[-1] == '-'): raise TypeError
source = source.replace("+", " + ")
source = source.replace("-", " - ")
source = source.split(" ")

soma = int(source[0])
for i in range(1, len(source), 2):
    if source[i] == "+":
        if source[i + 1] != "":
            soma += int(source[i + 1])
    elif source[i] == "-":
        if source[i + 1] != "":
            soma -= int(source[i + 1])
    else:
        raise TypeError
print(soma)