#!/usr/bin/env python

def get_abc(bias, key):
    a = ord('a')
    abc = ''.join([chr(i) for i in range(a, a+26)])
    for sym in key:
        abc = abc.replace(sym, '')
    abc = key + abc
    for i in range(bias):
        abc = abc[-1] + abc[:-1]
    return abc


inp = "input text"
bias = 3
key = "key"

abc = get_abc(bias, key)
message1 = ''
for sym in inp:
    if sym.isalpha():
        message1 += abc[(ord(sym) - 97)]
    else:
        message1 += sym
print(message1)
print(abc)
