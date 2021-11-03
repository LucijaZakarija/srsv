
import threading
from threading import Thread
import time
import random as rand
from queue import Queue




def info1():
    s=""
    sud=["a","p"]
    strana=["s","j","i","z"]
    prijelaz=["sj","js","iz","zi"]
    prvoS=rand.randint(0, 1)
    s+=sud[prvoS]
    drugoS=rand.randint(0, 3)
    s+=strana[drugoS]
    if sud[prvoS]=="a":
        if strana[drugoS]=="s":
           s+="sj"
        elif strana[drugoS]=="j":
           s+="js"
        elif strana[drugoS]=="i":
           s+="iz"
        elif strana[drugoS]=="z":
           s+="zi"
    else :
         if strana[drugoS]=="s" or strana[drugoS]=="j":
           l= rand.randint(2,3)
           s+=prijelaz[l]
         elif strana[drugoS]=="i" or strana[drugoS]=="z":

           l= rand.randint(0,1)
           s+=prijelaz[l]      
    
    return s

def sudionik(out_q,name,key,qSemP, qSemS,qRas): #zasad dobro radi
    out_q.put(name)
    qRas.put(name)
    #novo
    dict[key] = name
    dictV[key]=0
    a=True
    #print(name)
    while a:
       # qSemP.put(name) #ovdje je problem kome sem odg
        
        rez=0
        #print(i+"ovo je i")
        #print(dictV[key])
        if dictV[key]:
          rez=int(dictV[key])
        
        #print("ovo je rez"+str(rez))
        #if rez==0:
            #print("crveno :(, cekam "+str(key)+str(name))
        if rez==1:
            #print(name+"krece")
            #print("zeleno jupii "+str(key)+str(name)) #javlja ras da je dosao/posao
            qKrenuo.put(name)
            dict.pop(key)
            dictV.pop(key)
            if name[0]=="a":
              time.sleep(4)
            else:
              time.sleep(10)  
            qSisao.put(name)
            a=False
            #qSemS.task_done()
        else :
           time.sleep(1)
    return
   

def upr(in_q):
    a=True
    while a:
        data=in_q.get() #on dalje stavlja ciklusu da duze traje
        #print("tu sam "+str(data))
        if data[2]+data[3]=="sj" or  data[2]+data[3]=="js":
            stigao.put("sj")

        if data[2]+data[3]=="iz" or  data[2]+data[3]=="zi":
            stigao.put("iz")
             
        #a=False
        in_q.task_done()
        

    return

def ciklus(qS): #mijenja svjetla semafora
    lista=[]
    global IsSem
    while True:
      #slucaj 1
       semSJP=0
       semSJA=0
       semIZP=0
       semIZA=0
       ss=[semSJP,semSJA,semIZP,semIZA]
      
       IsSem="sve je crveno"
       qS.put(ss)
       sjZ=0
       izZ=0
       time.sleep(5) #svi izadu is raskrizja ako su u njemu

       while stigao.empty()==False:
        lista.append(stigao.get())  
       if lista.count("sj") > 0:
           sjZ=1
       if lista.count("iz") > 0:
           izZ=1
       lista.clear()


       k=5
       if izZ==1:
           k=20
           izZ=0
       semSJP=0
       semSJA=0
       #print(semSJP)      
       IsSem="IZ je zelen"
       semIZP=1
       semIZA=1
       ss=[semSJP,semSJA,semIZP,semIZA]
       qS.put(ss)



       time.sleep(k) 

       semSJP=0
       semSJA=0     
       IsSem="IZ za aute još uvijek zelen"
       semIZP=0
       semIZA=1
       ss=[semSJP,semSJA,semIZP,semIZA]
       qS.put(ss)
       time.sleep(10)

       semSJP=0
       semSJA=0
       semIZP=0
       semIZA=0
       ss=[semSJP,semSJA,semIZP,semIZA]
      
       IsSem="sve je crveno"
       qS.put(ss)
       time.sleep(5)
       while stigao.empty()==False:
        lista.append(stigao.get())  
       if lista.count("sj") > 0:
           sjZ=1

       lista.clear()
       k=5
       if sjZ==1:
           k=20
           sjZ=0
       #zeleno u frugom smjeru
       semSJP=1
       semSJA=1
       print(semSJP)      
       IsSem="SJ je zelen"
       semIZP=0
       semIZA=0
       ss=[semSJP,semSJA,semIZP,semIZA]
       qS.put(ss)
       time.sleep(k)

       semSJP=0
       semSJA=1
       #print(semSJP)      
       IsSem="SJ je zelen samo za aute"
       semIZP=0
       semIZA=0
       ss=[semSJP,semSJA,semIZP,semIZA]
       qS.put(ss)
       time.sleep(10)
    return


def sem(qSemP, qSemS,qSUp) :
    stanja=[0,0,0,0]
    
    while True:
       for x,y in list(dict.items()):
        data=y
        #print(y)
        #print(data)
        sud=data[0]
        poc=data[1]
        smjer=data[2]+data[3]
        if qSUp.empty()==False:
            stanja=qSUp.get()
            qSUp.task_done()
        #print("ovo su trneutna stanja"+str(stanja)+" a pojedinacno "+str(stanja[0])+str(stanja[1])+str(stanja[2])+str(stanja[3]) )

        if smjer=="sj" or smjer=="js":
           #print("ovo je smjer "+smjer)
           if sud=="p":
             #print("stavljam p "+str(stanja[0]))
             #qSemS.put(stanja[0])
             dictV[x]=stanja[0]
           elif sud=="a":
             #print("stavljam a "+str(stanja[1]))
            # qSemS.put(stanja[1])
             dictV[x]=stanja[1]

        if smjer=="iz" or smjer=="zi":
          # print("ovo je smjer  "+smjer)
           if sud=="p":
            # print("stavljam p "+str(stanja[2]))
             #qSemS.put(stanja[2])
             dictV[x]=stanja[2]
           elif sud=="a":
            # print("stavljam a "+str(stanja[3]))
            # qSemS.put(stanja[3])
             dictV[x]=stanja[3]
        
       #time.sleep(1)


def ras(qRas):
    cekanjePj=[" "," "," "," "," "," "," "," "]
    putujePj=[" "," "," "," "," "," "," "," "]
    dolaziAu=[" "," "," "," "]
    autiSJ=" "
    autiJS=" "
    autiIZ=" "
    autiZI=" "
    while True:
        ispis=[" "," "," "," "]#vidi hoce li ici ovako
        naCesti=[" "," "," "," "]
        sisao=[" "," "," "," "]
        if qRas.empty()==False: #vidi sto je sve doslo dok si spavao 1s NOVO
         ispis=qRas.get()
       
        if qKrenuo.empty()==False:
          naCesti=qKrenuo.get()
        if qSisao.empty()==False:
          sisao=qSisao.get()
        #print(str(ispis)+" u raskrizju")
        ispis1=ispis
        if ispis[0]=="p":
            if ispis[1]+ispis[2]=="si":
                cekanjePj[0]="p"
            if  ispis[1]+ispis[2]=="is":
                cekanjePj[2]="p"
            if ispis[1]+ispis[2]=="sz":
                cekanjePj[1]="p"
            if ispis[1]+ispis[2]=="zs":
                cekanjePj[3]="p"
            if ispis[1]+ispis[2]=="ji":
                cekanjePj[7]="p"
            if ispis[1]+ispis[2]=="ij":
                 cekanjePj[5]="p"
            if ispis[1]+ispis[2]=="jz":
                cekanjePj[6]="p"
            if ispis[1]+ispis[2]=="zj":
                cekanjePj[4]="p"

        
        ispis=naCesti
        if ispis[0]=="p":
            if ispis[1]+ispis[2]=="si":
                cekanjePj[0]=" "
                putujePj[0]="p"
            if  ispis[1]+ispis[2]=="is":
                cekanjePj[2]=" "
                putujePj[2]="p"
            if ispis[1]+ispis[2]=="sz":
                cekanjePj[1]=" "
                putujePj[1]="p"
            if ispis[1]+ispis[2]=="zs":
                cekanjePj[3]=" "
                putujePj[3]="p"
            if ispis[1]+ispis[2]=="ji":
                cekanjePj[7]=" "
                putujePj[7]="p"
            if ispis[1]+ispis[2]=="ij":
                 cekanjePj[5]=" "
                 putujePj[5]="p"
            if ispis[1]+ispis[2]=="jz":
                cekanjePj[6]=" "
                putujePj[6]="p"
            if ispis[1]+ispis[2]=="zj":
                cekanjePj[4]=" "
                putujePj[4]="p"

        ispis=sisao
        if ispis[0]=="p":
            if ispis[1]+ispis[2]=="si":
                putujePj[0]=" "
            if  ispis[1]+ispis[2]=="is":
                putujePj[2]=" "
            if ispis[1]+ispis[2]=="sz":
                putujePj[1]=" "
            if ispis[1]+ispis[2]=="zs":
                putujePj[3]=" "
            if ispis[1]+ispis[2]=="ji":
                putujePj[7]=" "
            if ispis[1]+ispis[2]=="ij":
                putujePj[5]=" "
            if ispis[1]+ispis[2]=="jz":
                putujePj[6]=" "
            if ispis[1]+ispis[2]=="zj":
                putujePj[4]=" "


       #dio za aute!
        ispis=ispis1
        if ispis[0]=="a":
            if ispis[2]+ispis[3]=="sj":
                dolaziAu[0]="A"
            if  ispis[2]+ispis[3]=="js":
                #print("auto se pojavilo js")
                dolaziAu[3]="A"
            if ispis[2]+ispis[3]=="iz":
                dolaziAu[2]="A"
            if ispis[2]+ispis[3]=="zi":
                dolaziAu[1]="A"
    
        ispis=naCesti
        if ispis[0]=="a":
            if ispis[2]+ispis[3]=="sj":
                autiSJ="A"
            if  ispis[2]+ispis[3]=="js":
               # print("auto js ide")
                autiJS="A"
            if ispis[2]+ispis[3]=="iz":
                autiIZ="A"
            if ispis[2]+ispis[3]=="zi":
                autiZI="A"
        ispis=sisao
        if ispis[0]=="a":
            if ispis[2]+ispis[3]=="sj":
                autiSJ=" "
                dolaziAu[0]=" "
            if  ispis[2]+ispis[3]=="js":
                autiJS=" "
                dolaziAu[3]=" "
            if ispis[2]+ispis[3]=="iz":
                autiIZ=" "
                dolaziAu[2]=" "
            if ispis[2]+ispis[3]=="zi":
                autiZI=" "
                dolaziAu[1]=" "

        if qRas.empty()==True and qKrenuo.empty()==True and qSisao.empty()==True:
         print(IsSem)
         print("        |"+dolaziAu[0]+"      |    ")
         print("       "+cekanjePj[0]+"|"+autiSJ+putujePj[0]+"   "+putujePj[1]+autiJS+"|"+cekanjePj[1]+"    ")
         print("       "+cekanjePj[2]+"|"+autiSJ+"     "+autiJS+"|"+cekanjePj[3]+"    ")
         print("________|"+autiSJ+"     "+autiJS+"|________")
         print("   "+autiIZ+autiIZ+autiIZ+autiIZ+putujePj[2]+autiIZ+autiIZ+autiIZ+autiIZ+autiIZ+"   "+putujePj[3]+autiIZ+autiIZ+autiIZ+autiIZ+dolaziAu[2])
         print(dolaziAu[1]+autiZI+autiZI+autiZI+autiZI+autiZI+autiZI+putujePj[4]+"        "+putujePj[5]+autiZI+autiZI+autiZI+autiZI+autiZI)
         print("________         ________")
         print("        |"+autiSJ+"     "+autiJS+"|    ")
         print("       "+cekanjePj[4]+"|"+autiSJ+"     "+autiJS+"|"+cekanjePj[5]+"    ")
         print("       "+cekanjePj[6]+"|"+autiSJ+putujePj[6]+"   "+putujePj[7]+autiJS+"|"+cekanjePj[7]+" ")
         print("        |      "+dolaziAu[3]+"|    ")
         print()
         print()
         time.sleep(1)


global dict
dict={}

global IsSem
IsSem=""

global dictV
dictV={}

global stigao
stigao=Queue()

broj_dretvi = rand.randint(5,15) #ove druge stvari vidi trebaju li biti global -.-
q = Queue()
qSUp = Queue()
global qPj
qPj=Queue()
global qSem,semSJP,semSJA,semIZP,semIZA
qSemP= Queue()
qSemS= Queue()
qRas= Queue()
global qKrenuo
global qSisao
qKrenuo=Queue()
qSisao=Queue()
#0 znaci crveno, 1 zeleno
semSJP=0
semSJA=0
semIZP=0
semIZA=0
t2 = Thread(target = upr, args =(q,))
t2.start()

tCiklus = Thread(target = ciklus, args =(qSUp,))
tCiklus.start()

tSem = Thread(target = sem, args =(qSemP, qSemS,qSUp))
tSem.start()

tRas = Thread(target = ras, args =(qRas,))
tRas.start()


for i in range(0,broj_dretvi):

        t1 = Thread(target = sudionik, args =(q,info1(),i,qSemP, qSemS,qRas))
        t1.start()
        time.sleep(rand.randint(1,5))
        if(i==5):
            time.sleep(40)


while threading.active_count() > 0:
    time.sleep(4)