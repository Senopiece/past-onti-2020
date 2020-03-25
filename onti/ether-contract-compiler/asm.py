#!/usr/bin/env python3

# ======================================== RULES ======================================== #
# используются только команды uint и не исключенные правилами таска!
# каждой команде своя строка
# все аргументы команде должны быть в её строке и через пробел: push 111
# после символа <#> и до конца строки транслятор не обрабатывает
# аргументы к командам указывать в десятичном формате: 
    # push 111 (само переведёт число в hex и закинет в байткод) >> 606F
# автомотическое определение размерности пуша (можно использовать без конкретной нотации): 
    # push 111 (автомотически воспринимается как PUSH1)
# автомотическое определение адреса на прыжок:
    # jumpdest a - метка куда прыгать ! обязательно только у jumpdest и как аргумент команды
    # ...
    # push a - подставление адреса команды по метке
    # jump
# ! в метке можно использовать сколько угодно символов, но только буквенных
# можно писать команды как заглавными, так и строчными буквами
# ======================================================================================== #

# used only push1
from sys import argv
from collections import defaultdict


global data
data = []

global marks
marks = defaultdict(str)


def to_hex(value):
    hexadecimal = hex(int(value))[2:].upper()
    if len(hexadecimal) % 2 != 0:
        return "0"+hexadecimal
    else:
        return hexadecimal

def decode(line):
    # preprocessing
    line = line.upper()
    line = line.strip()
    line = line.split('#')[0]
    parts = line.split()

    if len(parts) == 0:
        return

    # command detection
    command = parts[0]
    if command == "ADD":
        data.append("01")

    elif command == "PUSH":
        try:
            hexadecimal = to_hex(parts[1])
            n = len(hexadecimal) // 2

            data.append(to_hex(95+n))
            data.append(hexadecimal)
        except:
            data.append("?")
            data.append(parts[1])

    elif command == "JUMPDEST":
        if marks[parts[1]] != "":
            raise Exception("This mark already exist")
        marks[parts[1]] = to_hex(len(data))
        data.append("5B")

    elif command == "CALLDATALOAD":
        data.append("35")

    elif command.startswith("DUP"):
        n = ord(command[3])-ord('0')
        data.append(to_hex(127+n))

    elif command == "EQ":
        data.append("14")

    elif command == "JUMPI":
        data.append("57")

    elif command == "JUMP":
        data.append("56")

    elif command == "MSTORE":
        data.append("52")

    elif command == "RETURN":
        data.append("F3")

    elif command == "GT":
        data.append("11")

    elif command == "NOT":
        data.append("19")

    elif command.startswith("SWAP"):
        n = ord(command[4])-ord('0')
        data.append(to_hex(143+n))

    elif command == "DIV":
        data.append("04")

    else:
        raise Exception("Unknown command")

# read code form file
with open(argv[1], 'r') as f:
    line_num = 0
    for line in f:
        line_num += 1

        try:
            decode(line)
        except Exception as excptn:
            print(excptn, ">> line", line_num)

# postprocessing (insert marks)
bytecode = ""
i = 0
while i < len(data):
    if data[i] == "?":
        i += 1
        hexadecimal_mark_pc = marks[data[i]]
        n = len(hexadecimal_mark_pc) // 2
        bytecode += to_hex(95+n)+hexadecimal_mark_pc
    else:
        bytecode += data[i]
    i += 1


# output
print(bytecode)
