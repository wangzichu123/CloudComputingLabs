#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/time.h>
#include <pthread.h>
#include <queue>
#include <vector>
#include <iostream>
#include "mulsudoku.h"
using namespace std;

int numOfSolveThread = 2;
int total_solved = 0;
int total = 0;
bool (*solve)(int,job_t&) = mulsolve_sudoku_dancing_links;
FILE* fp;
char fileName[20];
char puzzle[128];

queue<struct job_t> job_queue;
priority_queue<struct job_t,vector<struct job_t>,cmp> result_queue;

pthread_mutex_t jobQueueMutex=PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t totalmutex=PTHREAD_MUTEX_INITIALIZER;

int64_t now()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec * 1000000 + tv.tv_usec;
}

void input(const char in[N],int* board)
{
  for (int cell = 0; cell < N; ++cell) 
 {
    board[cell] = in[cell] - '0';
    assert(0 <= board[cell] && board[cell] <= NUM);
    if(DEBUG_MODE)
    printf("%d",board[cell]);
  }
  if(DEBUG_MODE)
  printf("\n");
}

void* Solve(void* args) 
{
    while(1)
    {
	if(job_queue.size()<=0)
         	break;
        pthread_mutex_lock(&jobQueueMutex);
 	job_t t=job_queue.front();
 	job_queue.pop();
        pthread_mutex_unlock(&jobQueueMutex);
	
	if (solve(0,&t)) 
        {
           pthread_mutex_lock(&totalmutex);		
	   ++total_solved;
    	   pthread_mutex_unlock(&totalmutex);
	   result_queue.push(t);
        }
	else 
        { 
           printf("No: ");
	   for(int j=0;j<81;j++)
          	printf("%d",t.board[j]);		
	   printf("\n");
        }	
    }
}

int main(int argc, char* argv[])
{
  fp = fopen(fileName, "r"); 
   while (fgets(puzzle, sizeof puzzle, fp) != NULL) 
   {    
    	if (strlen(puzzle) >= N) 
   	{	
      		++total;
      		job_t j1;
      		j1.puzzleNo = total;
      		input(puzzle,j1.board); 
                job_queue.push(j1);
         }
   }
   if(DEBUG_MODE)
   printf("finish);
   fclose(fp);
  if (argv[1] != NULL)
  	numOfSolveThread = atoi(argv[1]);

  char a[20];
  cin>>a;
  strncpy(fileName,a+2,(sizeof a)-2);
  printf("fileName: %s", fileName);
  fp = fopen(fileName, "r");
  
  pthread_t ReaderThread;
  pthread_t SolveThread[numOfSolveThread];
  
  int64_t start = now();

  if(pthread_create(&ReaderThread, NULL, ReaderFuction, NULL)!=0)
  {
         perror("pthread_create failed");
         exit(1);
  }
  for(int i=0;i<numOfSolveThread;i++)
  {
    if(pthread_create(&SolveThread[i], NULL, Solve, NULL)!=0)
    {
         perror("pthread_create failed");
         exit(1);
    }
  }
  
  pthread_join(ReaderThread, NULL); 
  for(int i=0;i<numOfSolveThread;i++)
      pthread_join(SolveThread[i], NULL);  

  FILE * fp1;
  char resultFile[20];
  printf("file name ");
  cin>>resultFile;
  fp1 = fopen(resultFile, "r");
  while(!result_queue.empty())
  {
	job_t j1 = result_queue.top();
	result_queue.pop();
	
        for(int j=0;j<N;j++)
            fprintf(stdout,"%d",j1.board[j]);	
	fprintf(stdout,"\n");
   }
  fclose(fp1);

  int64_t end = now();
  double sec = (end-start)/1000000.0;
  printf("%f sec %f ms each %d\n", sec, 1000*sec/total, total_solved);
  
  return 0;
}


