#! /usr/bin/python
#coding: UTF-8
import argparse


# Запись в файл
def write(fname, code):
    outF = open(fname, 'wb')
    outF.write(''.join(code))


# Чтение из файла
def read(fname):
    try:
        with open(fname, 'rb') as inF:
            text = inF.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return text		


# Объявление аргументов
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inF')
    parser.add_argument('outF')
    return parser.parse_args()	
		

# циклический сдвиг влево на n бит
def rotateLeft(x, n): 
    return ((x << n) | (x >> (32-n))) & 0xFFFFFFFF 		
		
# Выравнивание потока и добавление длины сообщения
def alignment(msg):
    bytes = ""
    for i in range(len(msg)):
        bytes+='{0:08b}'.format(ord(msg[i]))
    bits = bytes + "1"
    Bits_ = bits
    while len(Bits_)%512 != 448:
        Bits_+= "0"

    Bits_+='{0:064b}'.format(len(bits) - 1)		
    return Bits_			
		
def rounds(buf, w):
    # 16 слов по 32-бита дополняются до 80 32-битовых слов:	
    for i in range(16, 80):
        w[i] = rotateLeft((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)
		
    # Инициализация хеш-значений этой части:
    a, b, c, d, e =  buf[0],  buf[1],  buf[2],  buf[3],  buf[4]

    #Главный цикл
    for i in range(0, 80):
        if 0 <= i <= 19:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d) 
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        temp = rotateLeft(a, 5) + f + e + k + w[i] & 0xffffffff
        e = d
        d = c
        c = rotateLeft(b, 30)
        b = a
        a = temp

    buf[0] = buf[0] + a & 0xffffffff
    buf[1] = buf[1] + b & 0xffffffff
    buf[2] =  buf[2] + c & 0xffffffff
    buf[3] =  buf[3] + d & 0xffffffff
    buf[4] = buf[4] + e & 0xffffffff

    return buf
	
	
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

		
def calc_sha1(data):
    # Шаг 1 Выравнивание потока
    # Шаг 2 Добавление длины сообщения
    data = alignment(data)
	
    # Шаг 3 Инициализация буфера
    buf = [0] * 5
    buf[0] = 0x67452301
    buf[1] = 0xefcdab89
    buf[2] = 0x98badcfe
    buf[3] = 0x10325476
    buf[4] = 0xc3d2e1f0
	
    # Шаг 4 Вычисление в цикле
  
    for i in chunks(data, 512): 
        words = chunks(i, 32)
        w = [0]*80
        for j in range(0, 16):
            w[j] = int(words[j], 2)
        buf = rounds(buf, w)
			
    # Шаг 5 Результат вычислений 

    res = ""
    for i in buf:
        res += "{:08x}".format(i)
		
    return res
	
	
def main():
    data = ""
    args = getArgs()
    data = read(args.inF)	
    res = calc_sha1(data)
    write(args.outF, res)
    print '\033[0;32mSuccess!\033[0m'
	
	
if __name__ == "__main__":
    main()	
