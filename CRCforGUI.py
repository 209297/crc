def strToPol(string):                                           #převod stringu čísel na výstup v polynomu
    lst = list(map(int, string))
    return np.poly1d(lst)

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