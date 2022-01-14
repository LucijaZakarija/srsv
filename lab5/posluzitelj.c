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

//ima dretvu ZAPRIMA
//ima dretve RADNE, krecemo samo s jednom

//zaprima cita iz reda poruka
//radna cita iz lok.spremnika i trazi u dijeljenom info

//TODO NAPRAVI LISTU I NAPRAVI VISE DRETVI
#define NAZIV_REDA "/lab5"
#define MAX_PORUKA_U_REDU 5
#define MAX_VELICINA_PORUKE 20

typedef struct Node {
    char * data;
    struct Node * next;
} node_t;

struct Node* head = NULL;
static sem_t sem; //globalna varijabla = za kazaljku na objekt u zajedničkoj memoriji
static sem_t sem_n;



void append(struct Node** head_ref, char * new_data)
{
    struct Node* new_node = (struct Node*) malloc(sizeof(struct Node));

    struct Node *last = *head_ref;  /* used in step 5*/

    new_node->data  = strdup(new_data);

    new_node->next = NULL;

    if (*head_ref == NULL)
    {
       *head_ref = new_node;
       //printf("lalala");
       return;
    }

    while (last->next != NULL)
        last = last->next;


    last->next = new_node;
    //printf("lilil");
    return;
    
    
    }
    

char* pop(struct Node** head_ref)
{
    // If linked list is empty
    if (*head_ref == NULL)
        return NULL;
 

    struct Node* temp = *head_ref;

         char * rez=temp->data;
        *head_ref = temp->next; // Change head
        free(temp); // free old head
        //printf("pop");
        return rez;
    
 
}




static void *radna_dretva ( void *id1 )  //vidi je li potrebno
{
int *n=id1;

sleep(1);
while(1){
sleep(1);
char * okolina=getenv("SRSV_LAB5");
  sem_wait(&sem);
  //sem_wait(&sem_n);
  if(head!=NULL) {
  char* rez=pop(&head); //if rez nije null!!!
  sem_post(&sem);
  
  //print_list(head); //print ne radi????
  //******UPISI U NEKI FIFO -> VJV LISTA
  //****ovaj dio inace radi RADNA dretva IZ LISTE CITA A NE OVAKO DIREKT!!!!!!!
  int id=0;
  int t=0;
  char ime[20];
  //sscanf(poruka, "%d %d %s", &id, &t, ime);
  sscanf(rez, "%d %d %s", &id, &t, ime);
  //printf("holaaa %d %d %s\n", id, t, ime);

  int * x;
  int id2=id;
/* svaki novi proces kre´ce sekundu kasnije */
  
  id = shm_open(ime, O_CREAT | O_RDWR, 00600);
  if (id == -1 || ftruncate(id, t) == -1) {
    perror("shm_open/ftruncate aaa");
    exit(1);
  }

  x = mmap(NULL, t, PROT_READ | PROT_WRITE, MAP_SHARED, id, 0);
  if (x == (void * ) - 1) {
    perror("mmap");
    exit(1);
  } else {
        //printf("Heeeej!! ja sam radna dretva u else\n");
      for (int i = 0; i < t; i++) {
        //printf("Heeeej!! ja sam radna dretva u petlji\n");
      printf("R%d: id:%d obrada podatka:%d  (%d/%d)\n",*n,id2,*x+i,i+1,t); //citanje memorije
      sleep(1);
    }

    shm_unlink(ime); 
  
  }
} else {
  sem_post(&sem); //da ne zaglavimo!!
   printf("R%d: Nema posla\n",*n);
  
}
}
}


int main(int argc, char *argv[]) {


  sem_init(&sem, 0, 1); //početna vrijednost = 1, 0=>za dretve SEMAFORRRR
  int i;
  int n=1; //broj radnih dretvi
  
  struct sched_param prio;
  int * BR;
  pthread_t * t;
  
  if (argc==2) {
  n=atoi(argv[1]);
  }
  sem_init(&sem_n, 0, n);
  //vrijeme
  srand(time(NULL));
  
  prio.sched_priority = 60;
  if (pthread_setschedparam(pthread_self(), SCHED_RR, &prio)) { //je li ok
        fprintf(stderr, "NEMA PRAVA\n");
        exit(1);
    }
  
  //stvori radne dretve i schedaj

  pthread_attr_t attr;
  pthread_attr_init(&attr);
  pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED); //????
  pthread_attr_setschedpolicy(&attr, SCHED_RR); //????
  prio.sched_priority = 40;
  pthread_attr_setschedparam(&attr, &prio);
  
  BR = malloc(n * sizeof(int));
  t = malloc(n * sizeof(pthread_t));
    for (i = 1; i < n + 1; i++) {
    BR[i - 1] = i; //thread id
    if (pthread_create( & t[i], &attr, radna_dretva, & BR[i - 1])) {  //stvori radne dretve
      fprintf(stderr, "Ne mogu stvoriti novu dretvu!\n"); 
      exit(1);
    }

  }

    
    //probno-> procitaj sadrzaj mem
    //******DRETVA ZAPRIMA*************
    sleep(1); //da sigurno gen prvo posalje
    while(1) {
 mqd_t opisnik_reda;
   char * okolina=getenv("SRSV_LAB5");
  char poruka[MAX_VELICINA_PORUKE];
  size_t duljina;
  unsigned prioritet; //NAZIV REDA
  opisnik_reda = mq_open(NAZIV_REDA, O_RDONLY);
  if (opisnik_reda == (mqd_t) - 1) {
    perror("potrosac:mq_open");
    return -1;
  }
  duljina = mq_receive(opisnik_reda, poruka, MAX_VELICINA_PORUKE, &
    prioritet);
  if (duljina < 0) {
    perror("mq_receive");
    return -1;
  }
  printf("P:Zaprimio: %s\n", poruka);
  //semaforrr
  sem_wait(&sem);
  append(&head,poruka);
  sem_post(&sem);
  
  
  }

  return 0;
}
