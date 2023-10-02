import numpy as np
from typing import Union
import math
import collections
import bitstring
import os
# Функция для чтения ключа Алисы из .bin файла


def read_keys(alice_key_path: str):
    res = []
    with open(alice_key_path, "rb") as file:
        hex = file.read().hex()
        bitarray = bitstring.BitArray(hex=hex).bin
        res.append(np.fromiter(bitarray, dtype=np.int8))
    return res


def bob_positions(filename):
    pos_list = []
    with open(filename, 'r') as f:
        for line in f:
            pos_list.append(int(line))
    f.close()
    return pos_list

# Функция для получения четности битов на позициях, которые прислал Боб


def get_alice_parity(positions, key):
    block = []
    for position in positions:
        block.append(key[position])
    if sum(block) % 2 == 0:
        return 0
    return 1


ali_read = read_keys("C:\\CascadeV4\\Data\\6%\\AliceKey.bin")
ali_list = ''
for i in ali_read[0]:
    ali_list += str(i)

pos = bob_positions("BobRequest.txt")

ali_list = [int(_) for _ in ali_list]

# Запись четности битов Алисы в файл для отправки бобу

with open("AliceAnswer.txt", 'w') as f:
    f.write(str(get_alice_parity(pos, ali_list)))
f.close()
