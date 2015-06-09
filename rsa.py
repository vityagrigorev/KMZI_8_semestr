#! /usr/bin/python
# coding: UTF-8

import argparse
import random


def writeFile(fname, code):
    try:
        with open(fname, 'wb') as f:
            f.write(''.join(code))
    except IOError:
        exit('No such file or directory ' + fname)		

		
def readFile(fname):
    try:
        with open(fname, 'rb') as f:
            text = f.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return text


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('outFile')
    parser.add_argument('mode', choices=['e', 'd'])
    return parser.parse_args()

	
# нахождение и проверка простого числа	
def PrimeN(bits):
    p = random.randint(2 ** (bits - 1), 2 ** bits)
    while not MillerRabin(p):
        p += 1
    return p	

	
# применение расширенного алгоритма Евклида	
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  
    else:
        return x % m

	
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
		

# тест Миллера-Рабина для проверки "простоты" числа
def MillerRabin(m):
    t = m - 1
    s = 0
    while t % 2 == 0:
        t /= 2
        s += 1
            
    for i in range(20):
        a = random.randint(2, m-2)
        x = pow(a, t, m)
        if x == 1:
            return True # составное
        for i in range(s - 1):
            x = (x ** 2) % m
            if x == m - 1:
                return True # составное
        return x == m - 1   # простое
				
		
# генерация ключей		
def KeyGen(bitlen):
    p = PrimeN(bitlen)
    q = PrimeN(bitlen)	
    while p == q:
        q = PrimeN(bitLen)
	# показываем ключи	
    print p	
    print q
    n = p * q # вычисляется модуль (произведение ключей)
    fi = (p-1) * (q-1) # вычисляется значение функции Эйлера
    e = 17  # простые числа Ферма 17, 257 или 65537 взаимнопростое с fi
    d = modinv(e, fi) # используем расширенный алгоритм Евклида
    pub_key = "{}\n{}".format(e, n) 
    priv_key = "{}\n{}".format(d, n)

    return 	pub_key, priv_key, n, e


def encryption (m, e, n):
    return pow(m, e, n)	# m^e mod n
	
def decryption (c, d, n):
    return pow(c, d, n)	
	
	
def main():
    print "RSA"
    bitlen = 1024 # заданный размер простых чисел
    kpub = "Public_key"
    kpriv = "Private_key"
    args = getArgs()

	#encrypt
    if args.mode == 'e':
        pub_key, priv_key, n, e = KeyGen(bitlen) # генерируем публичный и секретный ключи
        bytes = readFile(args.inFile) # читаем инфу с файла

        m = 0 # наше сообщение
        for i, c in enumerate(bytes):
            m |= (ord(c) << i*8)
        c = encryption(m, e, n)
        writeFile(args.outFile,str(c))
        writeFile(kpub, pub_key)
        writeFile(kpriv, priv_key)
    #decrypt
    if args.mode == 'd':
        f = open(kpriv)
        d = int(f.readline())
        n = int(f.readline())
        c = int(readFile(args.outFile)) 
        m = decryption(c, d, n)

        res = ""
        while m > 0: # переводим в читаемый вид
            byte = m % 256
            res += chr(byte)
            m /= 256

        writeFile(args.outFile, res)

		
if __name__ == "__main__":
    main()	
