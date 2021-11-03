Program je pisan u Pythonu na OS Windows.

Problem raskrižja riješen je pomoću dretvi, redova poruka i dijenjene memorije.
Dretve se stvaraju unutar petlje.

Na početku se definira slučajan broj dretvi koje nastaju u određenom slučajnom razmaku unutar petlje. Te dretve predstavljaju sudionike u prometu. Sudionik može biti pješak ili auto. Svaki sudionik ima informacije o njemu npr. assj definira auto koje se kreće od sjevera prema jugu, a psiz pješaka koji kreće sa si prema sz. Metoda koja se povezuje uz sudionike se zove sudionik i prima informacije o sudioniku, redni broj dretve i redove poruka uz pomoć koje sudionik komunicira sa semaforom, raskrižjem i upr.
Ostale dretve su:
ciklus - mijenja ciklus ovisno o broju pješaka/auta koji čekaju na zeleno.
upr - prima podatak od sudionika da je došao na raskrižje pomoću reda poruka i prosljeđuje informaciju ciklusu
sem - dretva koja simulira semafor, dobiva zahtjeve od sudionika pomoću globalne varijable koja predstavlja riječnik i odgovara s 1 ako sudionik smije preći cestu. Ispisuje kad dođe do promjene stanja na semaforu.
ras - dretva koja simulira  raskrižje. Od sudionika dobiva poruku kad je stvoren, kad kreće na cestu i kada je prošao raskrižje. Ispisuje stanje na raskrižju svake sekunde. Auti i pješaci prolaze kroz raskrižje 10s.
info1 - metoda uz pomoć koje se slučajno generiraju informacije o sudiniku


Opis rada raskrižja:
Stanja raskrižja su cccc-czcz-cccz-cccc-zczc-cczc-cccc
U slučaju da nikog nema na raskrižju:
crveno svima traj 5s, zatim 5s traje zeleno u smjeru i-z, zatim se pješacima i-z upali crveno, a autima ostane zeleno još 10s,nakon toga opet svi imaju crveno i postupak se ponavlja za smjer s-j. U slučaju da je bilo nekog na raskrižju zeleno će trajati 30s umjesto 10s. Pješacima treba 10s da pređu preko zebre, a autima treba 4s..