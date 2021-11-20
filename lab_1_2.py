#!/usr/bin/env python

abc = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
monograms = 'оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё'

text = ''

with open('text.txt', 'r') as f:
    text = f.read()
    text = "".join([c for c in text if c == ' ' or c == 'n' or c.isalpha()]).lower()
    offset = 3
    message = ''
    c = 0

for sym in text:
    if sym.isalpha():
        message += abc[(abc.find(sym) + offset) % 33]
    else:
        message += sym

monogram_frequencies = {}

for k in abc:
    monogram_frequencies[k] = 0

for sym in message:
    if sym != ' ':
        monogram_frequencies[sym] += 1

monogram_encode_map = ''
for offset, value in monogram_frequencies.items():
    i = 0
    while i < len(monogram_encode_map) and value <= monogram_frequencies[monogram_encode_map[i]]:
        i += 1
    monogram_encode_map = monogram_encode_map[:i] + offset + monogram_encode_map[i:]


mono_decoded = ''
for sym in message:
    if sym == ' ':
        mono_decoded += sym
    else:
        mono_decoded += monograms[monogram_encode_map.find(sym)]

print("Расшифровка монограммами: ", mono_decoded)

bigrams = {}
for i in range(len(text)-1):
    if text[i] == ' ' or text[i+1] == ' ':
        continue
    if text[i:i+2] not in bigrams.keys():
        bigrams[text[i:i+2]] = 1
    else:
        bigrams[text[i:i+2]] += 1

crypt_bigrams = {}
for i in range(len(message)-1):
    if message[i] == ' ' or message[i+1] == ' ':
        continue
    if message[i:i+2] not in crypt_bigrams.keys():
        crypt_bigrams[message[i:i+2]] = 1
    else:
        crypt_bigrams[message[i:i+2]] += 1

bigrams10 = []
for i in range(10):
    maxx = 0
    bigram = ''
    for offset, value in bigrams.items():
        if value > maxx:
            bigram = offset
            maxx = value
    bigrams10.append(bigram)
    bigrams.pop(bigram)

crypt_bigrams10 = []
for i in range(10):
    maxx = 0
    bigram = ''
    for offset, value in crypt_bigrams.items():
        if value > maxx:
            bigram = offset
            maxx = value
    crypt_bigrams10.append(bigram)
    crypt_bigrams.pop(bigram)

def move_two_letters(s, a, b):
    if a > b:
        a, b = b, a

    s1 = s[:a]
    s2 = s[a+1:b]
    s3 = s[b+1:]
    return s1 + s[b] + s2 + s[a] + s3

bigram_encode_map = monogram_encode_map

moved_letters = []
for i in range(len(bigrams10)):
    let1 = bigram_encode_map.find(crypt_bigrams10[i][0])
    let2 = monograms.find(bigrams10[i][0])
    if let1 != let2 and crypt_bigrams10[i][0] not in moved_letters:
        bigram_encode_map = move_two_letters(bigram_encode_map, let1, let2)
        moved_letters += bigram_encode_map[let1]
        moved_letters += bigram_encode_map[let2]

    let1 = bigram_encode_map.find(crypt_bigrams10[i][1])
    let2 = monograms.find(bigrams10[i][1])
    if let1 != let2 and crypt_bigrams10[i][1] not in moved_letters:
        bigram_encode_map = move_two_letters(bigram_encode_map, let1, let2)
        moved_letters += bigram_encode_map[let1]
        moved_letters += bigram_encode_map[let2]

decrypt_message2 = ''
for sym in message:
    if sym == ' ':
        decrypt_message2 += sym
    else:
        decrypt_message2 += monograms[bigram_encode_map.find(sym)]

print("Расшифровка биграммами: ", decrypt_message2)