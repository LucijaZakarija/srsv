import threading
from threading import Thread
import time
import random as rand
from queue import Queue



class Putnik:
    def __init__(self, ime, katP, katO,vrijeme):
        self.ime=ime
        self.p=katP
        self.o=katO
        self.time=vrijeme
        if katP<katO:
            self.smjer=1
        else:
            self.smjer=-1

    def __eq__(self, obj): #valjda nadjacava equals??????????
        return self.ime==obj.ime

def ispis():
    a=True
    
    while a:

       liftic=["        ","        ","        ","        "]
       iz=["","","",""]
       iz[kat-1]=izasli
       vozese="["
       for p in uLiftu:
           vozese+=p.ime
       vozese+="]"
       while len(vozese)<8:
           vozese+=" "
       liftic[kat-1]=vozese
       print("Smjer:"+str(smjer)+"   Vrata:Z") #namjesti da su vrata zatvorena/otvorena
       print("Stajanja        lift    Izašli")
       print4="kat4: "
       print3="kat3: "
       print2="kat2: "
       print1="kat1: "
       pomP="________________|        |____________"
       for p in prviK: #zasto nije definirano???????
           print1+=p.ime
       for p in drugiK:
            print2+=p.ime
       for p in treciK: #zasto nije definirano???????
           print3+=p.ime
       for p in cetvrtiK:
            print4+=p.ime
        
       while len(print1)<16:
           print1+=" "
       while len(print2)<16:
           print2+=" "
       while len(print3)<16:
           print3+=" "

       while len(print4)<16:
           print4+=" "

       print(print4+"|"+liftic[3]+"|"+str(iz[3]))
       print(pomP)
       print(print3+"|"+liftic[2]+"|"+str(iz[2]))
       print(pomP)
       print(print2+"|"+liftic[1]+"|"+str(iz[1]))
       print(pomP)
       print(print1+"|"+liftic[0]+"|"+str(iz[0]))
       print(pomP)
       print("Putnici")
       imena=""
       pocetak=""
       cilj=""

       for ptk in ukupno[:]:
           imena+=ptk.ime+" "
           pocetak+=str(ptk.p)+" "
           cilj+=str(ptk.o)+" "
       print(imena)
       print(pocetak)
       print(cilj)
       time.sleep(1)

    return


def lift():
    a=True
    vrata="Z" #na pocetku je lift na prvom katu sa zatvorenim vratima
    global kat
    kat=1
    odrediste=0
    #smjer=0 #stoji
    vrL=0
    brojLift=0
    idemPo=""
    global smjer
    global uLiftu
    global izasli
    while a:
        izasli=[]
        if smjer!=0: #ovo je slucaj u kojem se "krecem" uz pomoc INDEX nadi iz zahtjeva i makni
            if smjer==1 and kat!=4:
                kat+=1
            elif smjer==-1 and kat!=1:
                kat=kat-1
            #nakon sto smo povecali kat idemo pogledati tko je sve u liftu i treba li netko IZAC
            l=0
            for putnik in uLiftu[:]: #zbuni ga pop! ->pogledaj za druge
                #print(putnik.ime+"  "+str(putnik.o)+"na katu"+str(kat))
                if putnik.o==kat: #sad treba maknuti i iz one velike liste sve koji su izasli
                    #print("putnik "+str(putnik.ime)+" izlazi jer smo dosli na kat"+str(kat))
                    uLiftu.pop(uLiftu.index(putnik))

                    if ukupno.pop(ukupno.index(putnik)):
                       # print("aaaaaaaa")
                        izasli.append(putnik.ime)
                    
                    lif=""
                    for p in uLiftu:
                        lif+="### "+p.ime+" "+str(p.p)+" "+str(p.o)
                   # print("sadrzaj lifta "+lif)
                l+=1
                smjer=0 #??????????????

            ##print("ovo je odrediste"+odrediste)
            ##if kat==odrediste:
               ## print("istina")
               ## smjer=0

    
       # print("trenuto smo dosli na kat"+str(kat))
        if len(ukupno)>0:  #iz ukupno makni tek kad izade, nekako moras nac u listi koji je
            # print("stigao je zahtjev")
             prviZah=ukupno[0] #ovo kroz petlju #moram obrisati i ovo
             odrediste=prviZah.o
             idemPo=prviZah.ime
             #ukupno.pop(0)
             #ako lift nema smjer gleda prvi zahtjev i vrijeme
             #prvo lift stoji na svom katu i gleda ima li jos netko tu
             #ako ima i idu u smjeru kao on otvori vrata
             #pusti ih unutra
             #zatvori vrata i kreni
             if smjer==0 and len(uLiftu)==0: #lift je stajao i ima zahtjeva, ovo ispod se ionako nece izvrsiti inace
                 if(prviZah.p<kat):
                     
                     smjer=-1
                 elif prviZah.p>kat:
                     smjer=1
                 else:
                  if(prviZah.o<kat): #ako na prvom katu vec ima netko uci
                     
                     smjer=-1
                  elif prviZah.o>kat:
                     smjer=1
                # smjer=prviZah.smjer #njemu nije bitno tko ga je tocno pozvao samo smjer
                 #print(str(smjer)+"ovo je smjer")
                 odrediste=prviZah.o 
             elif smjer==0 and len(uLiftu)!=0:
                 zah=uLiftu[0]
                 if(zah.o<kat): #ako na prvom katu vec ima netko uci 
                     smjer=-1
                 elif zah.o>kat:
                     smjer=1
                 odrediste=zah.o 
                 
        if kat==1:
                    i=0
                    while len(uLiftu)<6 and len(prviK)>i:
                     if prviK[i].smjer==smjer or  (prviK[i].ime==idemPo and len(uLiftu)==0):
                        uLiftu.append(prviK[i])
                        #print("jupii usao je "+str(prviK[i].ime))
                        smjer=prviK[i].smjer
                        prviK.pop(i)
                        
                        i-=1
                     i+=1

        elif kat==2:
                    i=0
                    while len(uLiftu)<6 and len(drugiK)>i : #treba vidjeti je li kopija ili ne, ali otom potom
                     if drugiK[i].smjer==smjer  or  (drugiK[i].ime==idemPo and len(uLiftu)==0):
                      uLiftu.append(drugiK[i])
                      #print("jupii usao je "+str(drugiK[i].ime))
                      
                      smjer=drugiK[i].smjer
                      drugiK.pop(i)
                      i-=1
                     i+=1
                     
        elif kat==3:
                    i=0
                    while len(uLiftu)<6 and len(treciK)>i:
                      if treciK[i].smjer==smjer  or  (treciK[i].ime==idemPo and len(uLiftu)==0):
                        uLiftu.append(treciK[i])
                        #print("jupii usao je "+str(treciK[i].ime))
                        
                        smjer=treciK[i].smjer
                        treciK.pop(i)
                        i-=1
                      i+=1
        elif kat==4:
                    i=0
                    while len(uLiftu)<6 and len(cetvrtiK)>i: #i manja od i svaki
                     if cetvrtiK[i].smjer==smjer or (cetvrtiK[i].ime==idemPo  and len(uLiftu)==0):
                      uLiftu.append(cetvrtiK[i])
                      #print("jupii usao je "+str(cetvrtiK[i].ime))
                      
                      smjer=cetvrtiK[i].smjer
                      cetvrtiK.pop(i)
                      i-=1
                     i+=1
                     lif=""
        lif=""            
        for p in uLiftu:
                lif+="### "+p.ime+" "+str(p.p)+" "+str(p.o)
        #print("sadrzaj lifta nakon sto su svi usli"+lif)
        time.sleep(1)

        
    return

global prviK
prviK=[]
global drugiK
drugiK=[]
global treciK
treciK=[]
global cetvrtiK
cetvrtiK=[]
global ukupno
ukupno=[]

uLiftu=[]
izasli=[]
kat=1


smjer=0

prvi=0
drugi=0
treci=0
cetvrti=0

i=0
j=0
k=0
vrijeme=0
t = Thread(target = lift, args =())
t2 = Thread(target = ispis, args =())
t.start()
t2.start()
while i<40:
    i=i+1
    if j<25:
     ime=chr(97+j)
     j+=1
    else:
        ime=chr(65+k)
        k+=1
    poc=rand.randint(1,4)
    kraj=rand.randint(1,4)

    while kraj==poc: 
         kraj=rand.randint(1,4)
    #print("stvoren "+str(ime)+" "+str(poc)+" "+str(kraj))
    if poc==1:
      prviK.append(Putnik(ime,poc,kraj,vrijeme))  
    elif poc==2:
        drugiK.append(Putnik(ime,poc,kraj,vrijeme))  
    elif poc==3:
        treciK.append(Putnik(ime,poc,kraj,vrijeme))  
    elif poc==4:
        cetvrtiK.append(Putnik(ime,poc,kraj,vrijeme))  
    ukupno.append(Putnik(ime,poc,kraj,vrijeme))
    #san=poc=rand.randint(5,40)/10 #OVO ODREDUJE BRZINU STVARANJA PUTNIKA ->SPORA
    san=poc=rand.randint(3,15)/10 #->brza
    time.sleep(san)
    vrijeme+=san

    #putnik=Putnik(ime,poc,kraj)


