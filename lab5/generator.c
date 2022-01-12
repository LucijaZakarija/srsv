//generator stvara j poslova koji traju k vremena
//u aj spremniku za ime/id stvara prostor u koji upisuje trajanje
//salje opisnik posla u red poruka>njega prima u posl. zaprima

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <mqueue.h>
#include <time.h>
#include <string.h>


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <mqueue.h>
 #include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <mqueue.h>
#include <time.h>
#include <string.h>
#include <semaphore.h>

//#define NAZIV_ZAJ_SPREMNIKA "/fibonacci" /* napravljno u /dev/shm/ */
//#define VELICINA sizeof(struct dijeljeno)

//TODO VIDI KAKO TREBA ZAKLJUCATI U SLUCAJU VISE GENERATORA
#define BROJ_PROCESA 10
#define NAZIV_REDA "/lab5"
#define MAX_PORUKA_U_REDU 5
#define MAX_VELICINA_PORUKE 20


void posao_procesa(int proc_id,int vr) {
  //printf("tu sammm\n");
  char str[20];
  sprintf(str, "%d",proc_id+1);
  char * okolina=getenv("SRSV_LAB5");
  strcat(okolina,str);
  int id;
  int * x;
  sleep(proc_id); /* svaki novi proces kre´ce sekundu kasnije */
  
  id = shm_open(okolina, O_CREAT | O_RDWR, 00600);
  if (id == -1 || ftruncate(id, vr) == -1) {
    perror("shm_open/ftruncate");
    exit(1);
  }
  x = mmap(NULL, vr, PROT_READ | PROT_WRITE, MAP_SHARED, id, 0);
  if (x == (void * ) - 1) {
    perror("mmap");
    exit(1);
  }
  close(id);
  
  printf("G: posao %d %d %s [",proc_id+1, vr,okolina); 
    for (int i = 0; i < vr; i++) {
      x[i]=rand()%((200+1)-50) + 50; //zauzimanje memorije,valjda radi
      printf("%d ",*x+i);
    }
    printf("]\n");
  //printf("[%d] %d\n", proc_id + 1, x -> b);
  //printf ("The set path is: %s\n",okolina);
  //vjv error
  /* zadnji proces briše zajedniˇcki spremnik */
  sleep(1);
  if (proc_id == BROJ_PROCESA - 1) { //OVO POPRAVI
    munmap(x, vr);
    //printf("tu sam");
    shm_unlink(okolina);
  }
  /* ako se ne obriše, segment ostaje zauzet */
  
  
  //********SLANJE U RED PORUKA**************
  mqd_t opisnik_reda;
  struct mq_attr attr;
  char poruka[20];
  sprintf(poruka, "%d %d %s",proc_id+1,vr,okolina); //tekst poruke
  size_t duljina = strlen(poruka) + 1;
  unsigned prioritet = 50; //ovo cemo drugacije postavljati
  attr.mq_flags = 0;
  attr.mq_maxmsg = MAX_PORUKA_U_REDU;
  attr.mq_msgsize = MAX_VELICINA_PORUKE;
  char * red=getenv("SRSV_LAB5");
  opisnik_reda = mq_open(NAZIV_REDA, O_WRONLY | O_CREAT, 00600, & attr);
  if (opisnik_reda == (mqd_t) - 1) {
    perror("proizvodjac:mq_open");
    exit(1);
  }
  if (mq_send(opisnik_reda, poruka, duljina, prioritet)) {
    perror("mq_send");
    //return -1;
  }
  //printf("Poslano: %s [prio=%d]\n", poruka, prioritet);
}
int main(int argc, char *argv[]) {
printf("hej ho");
  srand(time(NULL));
  int i;
  int j=1; //broj poslova
  int k=1; //jedinica vremena
  //struct sched_param prio;
  printf("%d",argc);
  if (argc==3) {
  j=atoi(argv[1]);
  k=atoi(argv[2]);
  }
  //vrijeme
   /* prio.sched_priority = 60; KASNIJE
  if (pthread_setschedparam(pthread_self(), SCHED_RR, &prio)) { //je li ok
        fprintf(stderr, "NEMA PRAVA\n");
        exit(1);
    }*/
  
  for (i = 0; i < j; i++) {
  int vrijeme=rand()%((k+1)-1) + 1; //inace ce ici neki random?? da
    if (!fork()) {
      posao_procesa(i,vrijeme); //vidi hoce li trebati atoi() iz char-a
      sleep(1);
      exit(0);
    }
    }
  for (i = 0; i < BROJ_PROCESA; i++)
    wait(NULL);
    
   sleep(10);
  return 0;
}
