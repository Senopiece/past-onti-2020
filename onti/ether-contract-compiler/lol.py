#!/usr/bin/env python3

from math import log, floor

def to_hex(value):
    hexadecimal = hex(int(value))[2:].upper()
    if len(hexadecimal) % 2 != 0:
        return "0"+hexadecimal
    else:
        return hexadecimal

def bytes_len(value):
	# value > 0 !!!!!
	return floor(log(value, 256))+1

def pc_len(x_list):

for x_list in range(1):
	x_list = [23, 48, 56]
	n_ist = pc_len(x_list)
	print(n_ist)