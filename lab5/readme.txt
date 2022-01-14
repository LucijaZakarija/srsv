 Projekt se sastoji od 2 programa posluzitelj.c i generator.c
 Prevođenje: gcc -posluzitelj.c -o posluzitelj -lrt -pthread
             gcc -generator.c -o generator -lrt
 Pokretanje: sudo SRSV_LAB5=lab ./posluzitelj N (N je broj radnih dretvi)
            sudo SRSV_LAB5=lab ./generator J K (J je broj poslova, K je trajanje)
            
 Generator: generira J poslova velicine K, generira J polja velicine K. Svako polje popunjeno je random brojevima. U zajedničku memoriju koja je nastala kao var.okoline+redni broj posla upisuje to polje. U red poruka šalje ime zajedničke memorije, id posla i trajanje, ime reda poruka je srsv_lab5.
 
 Poslužitelj: ima dretvu za zaprimanje i N radnih dretvi. Dretva koja zaprima poruke iz reda poruka i  sprema ih u lokalnu memoriju, tj.listu. Za pristup listi koristi se semafor.
 Radne dretve pristupaju toj listi i gledaju ima li posla, u slučaju da ima iz liste uzimaju ime memorije i pristupaju mu. Nakon obrade posla dretve čekaju sljedeći zadatak. 
 Za raspoređivanje dretvi se također koristi prioriteti 40/50/60.
 
