import numpy as np
import itertools as it


def strToPol(string):                                           #převod stringu čísel na výstup v polynomu
    lst = list(map(int, string))
    return np.poly1d(lst)

def binInput(data):                                             #kontrola binárního vstupu
    isBin = False
    while isBin is not True:
        for i in range(len(data)):
            if (data[i] == ('1') or data[i] == ('0')):
                continue
            else:
                data = input("Zadejte pouze 0 nebo 1: ")
                break
        else:
            isBin = True
    return (data)

def intInput(data):                                             #kontrola číselného vstupu
    while True:
        if data.isnumeric():
            break
        else:
            data = input("Zadejte číslo: ")
    return int(data)

def hamming(k,r):                                               #kontrola zadání Hammingova kódu
    nInserted = k + r
    nHamming = (2**r)-1
    if nInserted == nHamming:
        print('\nZadali jste Hammingův kód.')
    else:
        print('\nNezadali jste Hammingův kód, program nemusí fungovat.')

def xor(a,b):                                                   #binární součet
    result = []
    for i in range(len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def binDiv(dividend, divisor):                                  #binární dělení
    x = len(divisor)
    temp = dividend[0:x]

    while x < len(dividend):
        if temp[0] == '1':
            temp = xor(temp, divisor) + dividend[x]
            temp = temp[1:(len(divisor)+1)]
        else:
            temp = temp + dividend[x]
            temp = temp[1:(len(divisor)+1)]
        x += 1
    if temp[0] == '1':
        temp = xor(divisor, temp)
        temp = temp[1:len(divisor)]
    else:
        temp = temp[1:len(divisor)]
    return temp

def genPol(r):                                                      #nalezení gen. polynomů
    binom = '1' + '0'*(n-1)  + '1'                                  #(z^n)-1
    allPol = list(map(list, it.product([0, 1], repeat=(r + 1))))    #všechny možné bin. kombinace délky (r+1)
    allPol = [''.join([str(j) for j in sublist]) for sublist in allPol]
    global genPols
    genPols = []
    for i in range(len(allPol)):
        if binDiv(binom,allPol[i]) == ('0' * r) and allPol[i][0]=='1':      #výběr gen. polynomů ze všech kombinací
            genPols.append(allPol[i])
    if genPols == []:
        print('\nNebyl nalezen žádný generující polynom.')
        quit()
    else:
        strGenPols = ', '.join(genPols)
        print('\nGenerující polynomy pro zvolené zabezpečení jsou: ', strGenPols)
        print('Polynomy uvedených generujících polynomů jsou:')
        for i in range(len(genPols)):
            print(strToPol(genPols[i]))

def checkPol(insertPol):                                #kontrola zadání gen. polynomu
    while True:
        if insertPol in genPols:
            break
        else:
            insertPol = input("Byl zadán špatný polynom. Vyberte z nabídky výše: ")
    return insertPol

def encode(message, genPoly):                           #zakódování zprávy
    sec = '0' * r
    data = message + sec
    remainder = binDiv(data, genPoly)
    encodedMsg = message + remainder
    return encodedMsg

def decode(delMessage, genPoly):                        #dekódování zprávy
    remainder = binDiv(delMessage, genPoly)
    if remainder == '0'*r:
        print('\nZpráva přijata bez chyby.')
        print('Polynom přijaté zprávy je: \n', strToPol(delMessage))
    else:
        pos = r                                                                 #pro chybu v informační části
        while pos < len(delMessage):
            pol = '1' + '0'* (pos)
            errorRem = binDiv(pol,genPoly)
            if remainder == errorRem:
                print('\nPřijatá zpráva obsahuje chybu na ', pos, '. pozici.')  #pozice zprava vč. nuly
                break
            else:
                pos += 1

        else:                                                                   #pro chybu v zabezp. části
            remainder=remainder[::-1]
            pos = remainder.find('1')
            print('\nPřijatá zpráva obsahuje chybu na ', (pos), '. pozici.')

        delMessage = delMessage[::-1]
        delMessage = list(delMessage)
        if delMessage[pos] == '0':
            delMessage[pos] = '1'
        else:
            delMessage[pos] = '0'

        delMessage = "".join(delMessage)
        delMessage = delMessage[::-1]
        print('Opravená zpráva je:', delMessage)
        print('Polynom opravené zprávy je: \n', strToPol(delMessage))

#_____________________________________________________________________

msg = input('Zadejte zprávu: ')
msg = binInput(msg)
k = len (msg)

r = (input('Zadejte počet zabezpečujících bitů: '))
r = intInput(r)
n = k + r
hamming(k,r)

genPol(r)
myPol = (input('\nVyberte jeden generující polynom: '))
myPol = checkPol(myPol)
print('Vybrali jste polynom ve tvaru: \n',strToPol(myPol))

encodedMsg = encode(msg,myPol)
print('\nZakódovaná zpráva je: ',encodedMsg)
print('Polynom zakódované zprávy je: \n',strToPol(encodedMsg))

delMsg = (input('\nJakou zprávu jste přijali? '))
delMsg = binInput(delMsg)
print('Polynom přijaté zprávy je: \n',strToPol(delMsg))
decode(delMsg,myPol)