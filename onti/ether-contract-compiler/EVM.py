from collections import defaultdict

# пока поддреживает только push1
# dup1-4 swap1-4

bytecode = input()
msg = list(map(int, input().split())) # значения отбельных блоков по 32 байта 

# preprocess
opcodes = [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]

# entry point
if __name__ == "__main__":
    stack = []
    mem = defaultdict(int) # каждая ячейка - uint 32 байта 
    pc = 0
    while pc < len(opcodes):
        opcode = opcodes[pc]
        if opcode == "01": #add
            stack.append(stack.pop() + stack.pop())
        elif opcode == "02": #mul
            stack.append(stack.pop() * stack.pop())
        elif opcode == "03": #sub
            stack.append(stack.pop() - stack.pop())
        elif opcode == "04": #div
            stack.append(stack.pop() // stack.pop())
        elif opcode == "60": #push1
            pc += 1
            stack.append(int(opcodes[pc], 16))
        elif opcode == "06": #mod
            stack.append(stack.pop() % stack.pop())
        elif opcode == "08": #addmod
            stack.append((stack.pop() + stack.pop()) % stack.pop())
        elif opcode == "09": #MULMOD
            stack.append((stack.pop() * stack.pop()) % stack.pop())
        elif opcode == "0A": #exp
            stack.append(stack.pop()**stack.pop())
        elif opcode == "10": #LT
            stack.append(stack.pop() < stack.pop())
        elif opcode == "11": #gt
            stack.append(stack.pop() > stack.pop())
        elif opcode == "14": #eq
            stack.append(stack.pop() == stack.pop())
        elif opcode == "15":
            stack.append(stack.pop() == 0)
        elif opcode == "16":
            stack.append(stack.pop() & stack.pop())
        elif opcode == "17":
            stack.append(stack.pop() | stack.pop())
        elif opcode == "18":
            stack.append(stack.pop() ^ stack.pop())
        elif opcode == "19":
            stack.append(~stack.pop())
        elif opcode == "1A": 
            i = stack.pop()
            x = stack.pop()
            stack.append((x >> (248 - i * 8)) & 0xFF)
        elif opcode == "18": 
            s = stack.pop()
            v = stack.pop()
            stack.append(v << s)
        elif opcode == "1C": 
            s = stack.pop()
            v = stack.pop()
            stack.append(v >> s)
        elif opcode == "35":
            i = stack.pop()
            stack.append(msg[i]) # для упрощения ввода и обработки оставим так
        elif opcode == "36":
            stack.append(len(msg)) # надеюсь эта команда никогда не будет использована
        elif opcode == "37":
            destOffset = stack.pop()
            offset = stack.pop()
            length = stack.pop()
            mem[destOffset:destOffset+length] = msg[offset:offset+length] # лень пилить, оставлю так
        elif opcode == "38":
            stack.append(len(opcodes))
        elif opcode == "39":
            pass # не думаю что нам пригодится
        elif opcode == "50":
            stack.pop()
        elif opcode == "51":
            stack.append(mem[stack.pop()])
        elif opcode == "52":
        	offset = stack.pop()
        	value = stack.pop()
            mem[offset] = value
        elif opcode == "56":
            pc = stack.pop()
        elif opcode == "57":
        	dst = stack.pop()
        	cond = stack.pop()
        	if cond:
        		pc = destination
        elif opcode == "5B": # JUMPDEST
            pass
        elif opcode == "80":
            stack.append(stack[-1])
        elif opcode == "81":
            stack.append(stack[-2])
        elif opcode == "82":
            stack.append(stack[-3])
        elif opcode == "83":
            stack.append(stack[-4])
        elif opcode == "90":
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif opcode == "91":
            stack[-1], stack[-3] = stack[-3], stack[-1]
        elif opcode == "92":
            stack[-1], stack[-4] = stack[-4], stack[-1]
        elif opcode == "93":
            stack[-1], stack[-5] = stack[-5], stack[-1]
        elif opcode == "F3":
        	o = stack.pop()
        	l = stack.pop() # ну, мы ожидаем, что тут у нас всегда 0x20
            print('returned', mem[o])# не забываем, что блоки у нас статичные, по 32 байта сразу
            break
        elif opcode == "FD":
            o = stack.pop()
        	l = stack.pop() # ну, мы ожидаем, что тут у нас всегда 0x20
        	# тут нужно перевернуть часть памяти, но мне лень. Если понадобится пишите...
        else:
            raise Exception("Провтив вас возбуждено уголовное дело по статье: "+str(opcode)+", pc="+str(pc))
        pc += 1
        print(pc, stack)