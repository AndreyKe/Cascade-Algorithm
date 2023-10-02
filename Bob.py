import math as m
import random
import numpy as np
from typing import Union
import math
import collections
import bitstring
import os
import time

# Функция для считывания .bin файла и записи его в строку


def read_keys(bob_key_path: str):
    res = []
    with open(bob_key_path, "rb") as file:
        # hint: if you need a smaller key - specify the number of bytes in read()
        hex = file.read().hex()
        bitarray = bitstring.BitArray(hex=hex).bin
        res.append(np.fromiter(bitarray, dtype=np.int8))

    return res


#  Функция для создания списка размеров блоков на каждой итерации


def get_k_list(q):
    # длины блоков k
    k1 = round(0.73 / q)
    k2 = k1 * 2
    k3 = k2 * 2
    k4 = k3 * 2
    return [k1, k2, k3, k4]

# Функция для сравнения ключей


def compare(a, b):
    count = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            count += 1
    return count / len(a) * 100

# Функция для разделения списка на части размерами К


def divide(k, positions, bits):
    indexes = [positions[i:i + k] for i in range(0, len(positions), k)]
    blocks = [bits[i:i + k] for i in range(0, len(positions), k)]
    return blocks, indexes

# Функция для разбиения списка на 2(с учетом того, что левая часть должна быть длиннее)


def split_list(my_list):
    middle = len(my_list) / 2
    a = my_list[:m.ceil(middle)]
    b = my_list[m.ceil(middle):]
    return a, b


# Функция для проверки четности битов Боба и сравнения с четностью битов Алисы


def bob_check(block, positions):
    # Запись позиций битов Боба, четность которых необходимо проверить
    with open("BobRequest.txt", "w") as f:
        for i in positions:
            f.write(str(i)+'\n')
    f.close()
    with open("Alice.py") as alice_programm:  # Запуск выполнения программы Алисы
        exec(alice_programm.read())
    with open("AliceAnswer.txt", "r") as f:  # Получение четности, вычислинной Алисой
        alice_parity = int(f.read())
    f.close()
    if sum(block) % 2 == alice_parity:
        return True  # четное колво ошибок
    else:
        return False  # нечетное колво ошибок

# Функция исполняющая бинарный алгоритм, позволяющий найти единичные ошибочные биты, возвращает позицию бита, который необходимо заменить


def binar(block, indexes):
    if len(block) == 1:  # Проверка длины блока
        if not bob_check(block, indexes):
            return indexes
    l, r = split_list(block)  # списки из битов l - левый r - правый
    li, ri = split_list(indexes)  # списки из индексов l - левый r - правый
    if bob_check(l, li):  # если левый четный, то
        return binar(r, ri)
    else:
        return binar(l, li)

# Основное тело программы


def main(q, bob_list):

    k_list = get_k_list(q)
    print(f'длины блоков: {k_list}\n')

    shuffled_indexes = list(range(len(bob_list)))

    i = 0
    prev_i = -1

    while i < len(k_list):
        if i > prev_i and i > 0:
            random.shuffle(shuffled_indexes)
            # print('пошалил) в i =', i)

        current_list = [bob_list[i] for i in shuffled_indexes]

        # делим на блоки
        blocks, indexes = divide(k_list[i], shuffled_indexes, current_list)

        indexes_to_change = []
        change_iter = 0
        for block, index in zip(blocks, indexes):
            if not bob_check(block, index):
                # print(i, end='')
                indexes_to_change += binar(block, index)
                if i > 0:
                    change_iter = -2
        # print('')
        for index in indexes_to_change:
            bob_list[index] = int(not bob_list[index])
        current_list = [bob_list[i] for i in shuffled_indexes]

        print(
            f'Итерация: {i}\nСовпадение после итерации %: {compare(bob_list, ali_list):.2f}\n')

        prev_i = i
        i += 1 + change_iter
    bob_str = ''
    for i in bob_list:
        bob_str += str(i)
    with open("bob_final_list.txt", 'w') as f:
        f.write(bob_str)


# Считывание ключей Алисы и Боба

start = time.time()

bob_read = read_keys("C:\\CascadeV4\\Data\\6%\\BobKey.bin")
bob_list = ''
for i in bob_read[0]:
    bob_list += str(i)
ali_read = read_keys("C:\\CascadeV4\\Data\\6%\\AliceKey.bin")
ali_list = ''
for i in ali_read[0]:
    ali_list += str(i)

# Сравнение ключей
print(f'Первичное совпадение: {compare(ali_list, bob_list):.2f}%')

# Определение QBER

Q = (100 - compare(ali_list, bob_list))/100
print("Значение QBER:", Q*100, "%")

with open("AliKey.txt", 'w') as f:
    f.write(ali_list)

# Приведение ключей к типу int для удобства работы с ними
ali_list = [int(_) for _ in ali_list]
bob_list = [int(_) for _ in bob_list]


# длины ключей до выполнения алгоритма

print("Длина ключа Алисы до выполнения алгоритма:", len(ali_list))
print("Длина ключа Боба до выполнения алгоритма:", len(bob_list))

# Ввод QBER c клавиатуры в случае работы рельной программы, если Бобу Нельзя иметь доступ к ключу Алисы

# print("Введите QBER в %")
# Q = input()/100


if __name__ == '__main__':
    main(Q, bob_list)

# длины ключей после выполнения алгоритма

print("Длина ключа Алисы после выполнения алгоритма:", len(ali_list))
print("Длина ключа Боба после выполнения алгоритма:", len(bob_list))


print('Выполнение закончено')
end = time.time() - start
print("Время выполнения:", end)
