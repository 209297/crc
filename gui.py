from tkinter import *
from tkinter import messagebox
import itertools as it
from CRCforGUI import xor
from CRCforGUI import binDiv
import os
import sys
#_______________________________________
window = Tk()
window.geometry('1100x500')
window.title('CRC')

icon = PhotoImage(file='VTI.png')
window.iconphoto(True, icon)
window.config(background='#5F9CAF')

def binInput(data_,entry, isBin):
    isBin
    while isBin is not True:
        for i in range(len(data_)):
            if (data_[i] == ('1') or data_[i] == ('0')):
                continue
            else:
                messagebox.showinfo('Nesprávný formát','Zadejte pouze 0 nebo 1.')
                data_=None
                break
        else:
            isBin = True
    return(data_)

def hamming(k,r):
    nInserted = k + r
    nHamming = (2**r)-1
    if nInserted == nHamming:
        hamLabel = Label(window, text='Zadali jste Hammingův kód.', font=('Calibri', 12), bg='#5F9CAF', pady=10)
        hamLabel.grid(row=6, column=1)
    else:
        hamLabel = Label(window, text='Nezadali jste Hammingův kód,\nprogram nemusí fungovat.',
                         font=('Calibri', 12),bg='#5F9CAF', pady=10)
        hamLabel.grid(row=6, column=1)

def genPol(r):
    binom = '1' + '0'*(n-1)  + '1'
    allPol = list(map(list, it.product([0, 1], repeat=(r + 1))))
    allPol = [''.join([str(j) for j in sublist]) for sublist in allPol]
    global genPols
    genPols = []
    for i in range(len(allPol)):
        if binDiv(binom,allPol[i]) == ('0' * r) and allPol[i][0]=='1':
            genPols.append(allPol[i])
    if genPols == []:
        genPolLabel = Label(window, text='Nebyl nalezen žádný generující polynom.', font=('Calibri', 12), bg='#5F9CAF', pady=10)
        genPolLabel.grid(row=7, column=1)
    else:
        strPolynoms=StringVar()
        strGenPols = ', '.join(genPols)
        genPolLabel = Label(window, textvariable=strPolynoms, font=('Calibri', 12),bg='#5F9CAF', padx=10,pady=10)
        genPolLabel.grid(row=7, column=1)
        strPolynoms.set(str('Generující polynomy pro zvolené zabezpečení jsou: \n\n'+(strGenPols)))

#_________________________________________________________________
def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

msgVar=StringVar()
isBinary=False
def submitmsg():
    global msg
    global msgVar
    msg = msgentry.get()
    msgentry.delete(0, END)
    binInput(msg, msgentry, isBinary)
    if isBinary == True:
        msgVar.set(msg)
    else:
        binInput(msg, msgentry, isBinary)
    msgL = Label(window, textvariable=msgVar, font=('Calibri', 12), bg='#5F9CAF')
    msgL.grid(row=1, column=1, padx=10, pady=20)
    msgVar.set(str(msg))
    msgentry.destroy()
    msgsubmit.destroy()
    global k
    k=len(msg)
    rentry.focus_set()

rVar=IntVar()
def submitr():
    global r
    r = rentry.get()
    rentry.delete(0, END)
    while True:
        if r.isnumeric():
            rVar.set(r)
            break
        else:
            messagebox.showinfo('Nesprávný formát', 'Zadejte číslo.')
            r=None
    rvlabel = Label(window, textvariable=rVar, font=('Calibri', 12), bg='#5F9CAF', width=40)
    rvlabel.grid(row=3, column=1)
    rVar.set(str(r))
    rentry.destroy()
    rsubmit.destroy()
    r=int(r)
    global n
    n = k + r
    hamming(k,r)
    genPol(r)
    myPollabel = Label(window, text='Vyberte generující polynom: ', font=('Calibri', 12), bg='#5F9CAF', padx=10,
                       pady=20)
    myPollabel.grid(row=8, column=0)

    global myPolentry
    myPolentry = Entry(window, font=('Calibri', 12), width=42)
    myPolentry.grid(row=8, column=1)
    myPolentry.bind('<Return>', submitPol)

    global myPolsubmit
    myPolsubmit = Button(window, text='Odeslat', command=submitPol)
    myPolsubmit.grid(row=8, column=2, padx=10, pady=10)
    myPolentry.focus_set()

myPolVar=StringVar()
myPol=str()
def submitPol():
    global myPol
    myPol = myPolentry.get()
    myPolentry.delete(0, END)
    while True:
        if myPol in genPols:
            myPolVar.set(myPol)
            pollabel = Label(window, textvariable=myPolVar, font=('Calibri', 12), bg='#5F9CAF', width=40)
            pollabel.grid(row=8, column=1)
            myPolVar.set(str(myPol))
            myPolentry.destroy()
            myPolsubmit.destroy()
            encodeButton = Button(window, text='Zakódovat zprávu', command=encode)
            encodeButton.grid(row=9, column=1, padx=10, pady=10)
            window.focus_set()
            break
        else:
            messagebox.showinfo('Nesprávný polynom','Byl zadán špatný polynom. Vyberte polynom z nabídky.')
            break

encodedMsgVar=StringVar()
def encode():
    sec = '0' * r
    data = msg + sec
    remain = binDiv(data, myPol)
    encodedMsg = msg + remain
    encodedMsgVar.set(encodedMsg)
    encodedLabel = Label(window, textvariable=encodedMsgVar, font=('Calibri', 13, 'bold'), bg='#5F9CAF', pady=10)
    encodedLabel.grid(row=9,column=1)
    encodedMsgVar.set(str('Zakódovaná zpráva je : ' + (encodedMsg)))

    delMsglabel = Label(window, text='Jakou zprávu jste přijali?', font=('Calibri', 12), width=30,bg='#5F9CAF', padx=10, pady=10)
    delMsglabel.grid(row=1, column=4)

    global delMsgentry
    delMsgentry = Entry(window, font=('Calibri', 12), width=40)
    delMsgentry.grid(row=3, column=4)
    delMsgentry.bind('<Return>', submitdelMsg)

    global delMsgsubmit
    delMsgsubmit = Button(window, text='Dekódovat', command=submitdelMsg)
    delMsgsubmit.grid(row=4, column=4)

delMsgVar=StringVar()
posVar=IntVar()
isDelBinary = False
def submitdelMsg():
    global delMsg
    global delMsgVar
    delMsg = delMsgentry.get()
    delMsgentry.delete(0, END)
    binInput(delMsg, delMsgentry, isDelBinary)
    if isDelBinary == True:
        delMsgVar.set(delMsg)
        delMsglabel = Label(window, textvariable=delMsgVar, font=('Calibri', 12), bg='#5F9CAF', width=40)
        delMsglabel.grid(row=2, column=4)
        delMsgVar.set(str('Doručená zpráva je: ' + (delMsg)))
    else:
        binInput(delMsg, delMsgentry,isDelBinary)

    remaindermsg = binDiv(delMsg, myPol)
    if remaindermsg =='0'*r:
        noErLabel = Label(window, text='Zpráva přijata bez chyby.', font=('Calibri', 12, 'bold'), bg='#5F9CAF', pady=10)
        noErLabel.grid(row=3, column=4)
    else:
        pos = r
        while pos < len(delMsg):
            pol = '1' + '0' * (pos)
            errorRem = binDiv(pol, myPol)
            if remaindermsg == errorRem:
                strPos = str(pos)
                posVar.set(strPos)
                erLabel = Label(window, textvariable=posVar, font=('Calibri', 12), bg='#5F9CAF', padx=10,pady=10)
                erLabel.grid(row=3, column=4)
                posVar.set(str('Přijatá zpráva obsahuje chybu na ' + (strPos) + '. pozici zprava.'))
                break
            else:
                pos += 1
        else:
            remaindermsg = remaindermsg[::-1]
            pos = remaindermsg.find('1')
            strPos=str(pos)
            posVar.set(strPos)
            errorLabel = Label(window, textvariable=posVar, font=('Calibri', 12), bg='#5F9CAF', padx=10,pady=10)
            errorLabel.grid(row=3, column=4)
            posVar.set(str('Přijatá zpráva obsahuje chybu na '+(strPos)+'. pozici zprava.'))

        delMsg = delMsg[::-1]
        delMsg = list(delMsg)
        if delMsg[pos] == '0':
            delMsg[pos] = '1'
        else:
            delMsg[pos] = '0'
        delMsg = "".join(delMsg)
        delMsg = delMsg[::-1]
        delMsgVar.set(delMsg)
        delMsgVar.set(str('Opravená zpráva je: '+(delMsg)))
        corr = Label(window, textvariable=delMsgVar, font=('Calibri', 13, 'bold'), bg='#5F9CAF', pady=10)
        corr.grid(row=4, column=4)
        window.focus_set()

#_____________________________________________________________
labelCRC = Label(window, text='CRC', font=('Georgia',20,'bold'),bg='#5F9CAF', pady=30)
labelCRC.grid(row=0,column=1,columnspan=4)


msglabel = Label(window, text='Zadejte zprávu:',font=('Calibri',12),width=25,bg='#5F9CAF',padx=10, pady=20)
msglabel.grid(row=1,column=0)

msgentry = Entry(window, font=('Calibri',12),width=42)
msgentry.grid(row=1,column=1, padx=10, pady=0)
#msgentry.bind('<Return>',submitmsg)

msgsubmit = Button(window,text='Odeslat',command=submitmsg)
msgsubmit.grid(row=1,column=2, padx=10, pady=10)


rlabel = Label(window, text='Zadejte délku zabezpečení:',font=('Calibri',12),bg='#5F9CAF',padx=10, pady=20)
rlabel.grid(row=3,column=0)

rentry = Entry(window, font=('Calibri',12),width=42)
rentry.grid(row=3,column=1)
#rentry.bind('<Return>', submitr)

rsubmit = Button(window,text='Odeslat',command=submitr)
rsubmit.grid(row=3,column=2, padx=10, pady=10)

blank= Label(window, width=40,bg='#5F9CAF')
blank.grid(row=3, column=4)

restart=Button(window,text="Restartovat program", command=restart)
restart.grid(row=9,column=5)

window.mainloop()