from web3 import Web3
from collections import defaultdict
from ether_bridge.EthAccountBridge import EthAccountBridge
from ether_bridge.EthSession import EthSession

used_contracts = []

session = EthSession('https://sokol.poa.network')
acc = session.Account('5675eff7ed6e5ef339e7bc464d28f78ad306da8bdf53b10d36be27fff74fc7c2')

def emulate_evm(contract_address, msg, contract_caller=None):
    bytecode = session.web3.eth.getCode(contract_address).hex()[2:].upper()
    temporary_storage = defaultdict(lambda: None)
    returndata = bytes()
    _lenret = 0

    # preprocess
    opcodes = [bytecode[i:i+2] for i in range(0, len(bytecode), 2)]
    actual_bytecode = bytes.fromhex(bytecode)

    # execution
    stack = []
    mem = bytearray(1024)
    pc = 0
    while pc < len(opcodes):
        opcode = opcodes[pc]
        byte_value = int(opcode, base=16)
        if opcode == "00": #stop
            return (0, b'')
        elif opcode == "01": #add
            stack.append(stack.pop() + stack.pop())
        elif opcode == "02": #mul
            stack.append(stack.pop() * stack.pop())
        elif opcode == "03": #sub
            stack.append(stack.pop() - stack.pop())
        elif opcode in ("04", "05"): #div
            stack.append(stack.pop() // stack.pop())
        elif opcode in ("06", "07"): #mod
            stack.append(stack.pop() % stack.pop())
        elif opcode == "08": #addmod
            stack.append((stack.pop() + stack.pop()) % stack.pop())
        elif opcode == "09": #MULMOD
            stack.append((stack.pop() * stack.pop()) % stack.pop())
        elif opcode == "0A": #exp
            stack.append(stack.pop()**stack.pop())
        elif opcode in ("10", "12"): #LT
            stack.append(stack.pop() < stack.pop())
        elif opcode in ("11", "13"): #gt
            stack.append(stack.pop() > stack.pop())
        elif opcode == "14": #eq
            stack.append(stack.pop() == stack.pop())
        elif opcode == "15": #ISZERO
            stack.append(stack.pop() == 0)
        elif opcode == "16": # and
            stack.append(stack.pop() & stack.pop())
        elif opcode == "17": # or
            stack.append(stack.pop() | stack.pop())
        elif opcode == "18": # xor
            stack.append(stack.pop() ^ stack.pop())
        elif opcode == "19": # not
            stack.append(~stack.pop())        
        elif opcode == "1A":
            i = stack.pop()
            x = stack.pop()
            stack.append((x >> (248 - i * 8)) & 0xFF)
        elif opcode == "1B":
            shift = stack.pop()
            value = stack.pop()
            stack.append(value << shift)
        elif opcode in ("1C", "1D"):
            shift = stack.pop()
            value = stack.pop()
            stack.append(value >> shift)
        elif opcode == "20":
            o = stack.pop()
            l = stack.pop()
            stack.append(int(acc.w3.keccak(bytes(mem[o:o+l])).hex(), 16))
        elif opcode == "30":
            stack.append(int(contract_address))
        elif opcode == "31":
            addr = session.web3.toChecksumAddress(hex(stack.pop()).ljust(42, '0'))
            stack.append(acc.w3.eth.getBalance(addr))
        elif opcode == "32":
            stack.append(int(acc.address))
        elif opcode == "33":
            stack.append(int(contract_caller) if contract_caller is not None else int(acc.address))
        elif opcode == "34":
            stack.append(0)
        elif opcode == "35":
            i = stack.pop()
            stack.append(int.from_bytes(msg[i:i+32], "big"))
        elif opcode == "36":
            stack.append(len(msg))
        elif opcode == "37":
            destOffset = stack.pop()
            offset = stack.pop()
            length = stack.pop()
            mem[destOffset:destOffset+length] = msg[offset:offset+length]
        elif opcode == "38":
            print('opcodes len: ', len(opcodes), len(actual_bytecode))
            stack.append(len(opcodes))
        elif opcode == "39":
            destOffset = stack.pop()
            offset = stack.pop()
            length = stack.pop()
            mem[destOffset:destOffset+length] = actual_bytecode[offset:offset+length]
        elif opcode == "3A":
            print('gasPrice used')
            stack.append(acc.w3.eth.gasPrice)
        elif opcode == "3B":
            addr = session.web3.toChecksumAddress(hex(stack.pop()).ljust(42, '0'))
            stack.append((len(session.web3.eth.getCode(addr).hex()) // 2) - 1)
        elif opcode == "3C":
            print('bad using there (place #bob)')
            addr = session.web3.toChecksumAddress(hex(stack.pop()).ljust(42, '0'))
            destOffset = stack.pop()
            offset = stack.pop()
            length = stack.pop()
            mem[destOffset:destOffset+length] = bytes.fromhex(session.web3.eth.getCode(addr).hex())[offset:offset+length]
        elif opcode == "3D":
            stack.append(_lenret) # maybe len(returndata)
        elif opcode == "3E":
            destOffset = stack.pop()
            offset = stack.pop()
            length = stack.pop()
            mem[destOffset:destOffset+length] = returndata[offset:offset+length]
        elif opcode == "3F":
            addr = hex(stack.pop()).ljust(42, '0')
            if acc.w3.isAddress(addr):
                stack.append( int(acc.w3.keccak(addr).hex(), 16) )
            else:
                stack.append(0)
        elif opcode == "50":
            stack.pop()
        elif opcode == "51":
            stack.append(mem[stack.pop()])
        elif opcode == "52":
            offset = stack.pop()
            value = stack.pop()
            mem[offset:offset+32] = value.to_bytes(32, byteorder='big')
        elif opcode == "53":
            offset = stack.pop()
            value = stack.pop()
            mem[offset] = value % 256
        elif opcode == "54":
            key = stack.pop()
            if temporary_storage[key] is None:
                stack.append(int(session.web3.eth.getStorageAt(contract_address, key).hex(), 16))
            else:
                stack.append(temporary_storage[key])
        elif opcode == "55":
            key = stack.pop()
            value = stack.pop()
            temporary_storage[key] = value
        elif opcode == "56":
            pc = stack.pop() - 1
        elif opcode == "57":
            dest = stack.pop()
            cond = stack.pop()
            if cond:
                pc = dest - 1
        elif opcode == "58":
            stack.append(pc)
        elif opcode == "59":
            stack.append(len(mem))
        elif opcode == "5A":
            stack.append(1000000000)
        elif opcode == "5B": # JUMPDEST
            pass
        elif byte_value >= 96 and byte_value <= 127: # PUSH N
            N = byte_value - 95
            stack.append(int(''.join(opcodes[pc+1:pc+N+1]), 16))
            pc += N
        elif byte_value >= 128 and byte_value <= 143: # DUP N
            N = byte_value - 127
            stack.append(stack[-N])
        elif byte_value >= 144 and byte_value <= 159: # SWAP N
            N = byte_value - 142
            stack[-1], stack[-N] = stack[-N], stack[-1]
        elif opcode == "FA":
            _ = stack.pop() # gas
            addr = session.web3.toChecksumAddress(hex(stack.pop()).ljust(42, '0'))
            if addr not in used_contracts:
                used_contracts.append(addr)
            argsOffset = stack.pop()
            argsLength = stack.pop()
            retOffset = stack.pop()
            retLength = stack.pop()
            success, returndata = emulate_evm(addr, bytes(mem[argsOffset:argsOffset+argsLength]), contract_caller=contract_address)
            if len(returndata) > retLength:
                raise Exception('len(returndata) > retLength')
            mem[retOffset:retOffset+retLength] = returndata
            _lenret = retLength
            stack.append(success)
        elif opcode == "F3":
            o = stack.pop()
            l = stack.pop()
            return (1, mem[o:o+l])
        elif opcode == "FD":
            o = stack.pop()
            l = stack.pop()
            return (0, mem[o:o+l])
        else:
            raise Exception("Неизвестный опкод: "+opcode+", pc="+hex(pc)[2:].upper())
        #print(opcode, stack)
        #print()
        #input()
        pc += 1
        #print("pc:", hex(pc)[2:].upper())


# entry point
if __name__ == "__main__":
    contract_address = input('contract addr: ')
    msg = input('msg: ')

    #res = acc.call({
    #     'to': contract_address,
    #     'data': msg
    # })
    # print(res)

    if msg.startswith('0x'):
        msg = msg[2:]
    msg = bytes.fromhex(msg)

    used_contracts.append(contract_address)
    print(emulate_evm(contract_address, msg))
    print()

    used_contracts.sort()
    for contract in used_contracts:
        print(contract)
