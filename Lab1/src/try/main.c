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
#include "sudoku.h"
using namespace std;

int numOfSolveThread = 2;
int total_solved = 0;
int total = 0;
bool (*solve)(int,int*) = solve_sudoku_dancing_links;
char fileName[20];
char puzzle[128];
FILE* fp;

struct job_t
{
	int No;	//题目在输入文件中的编号
	int board[81];  //题目
};

queue<struct job_t> job_queue;
struct cmp
{
    bool operator() (job_t job1,job_t job2)      //最小编号优先级最高
    {
        return job1.No > job2.No;
    }
};
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
    printf("%d",board[cell]); //打印读入的题
  }
  if(DEBUG_MODE)
  printf("\n"); //打印读入的题
}

void* ReaderFuction(void* args) 
{
   fp = fopen(fileName, "r"); 
   while (fgets(puzzle, sizeof puzzle, fp) != NULL) 
   {    
    	if (strlen(puzzle) >= N) 
   	{	
      		++total;
      		job_t j1;
      		j1.No = total;
      		input(puzzle,j1.board); 
                job_queue.push(j1);
         }
   }
   if(DEBUG_MODE)
   printf("读文件完毕");
   fclose(fp);
}

void* SolveFuction(void* args) 
{
    while(1)
    {
	if(job_queue.size()<=0)
         	break;
        pthread_mutex_lock(&jobQueueMutex);
 	job_t j1=job_queue.front();
 	job_queue.pop();
        pthread_mutex_unlock(&jobQueueMutex);
	
	if (solve(0,j1.board)) 
        {
           pthread_mutex_lock(&totalmutex);		
	   ++total_solved;
    	   pthread_mutex_unlock(&totalmutex);
	   result_queue.push(j1);
        }
	else 
        {  //solve返回了false 表示无解
           printf("No: ");
	   for(int j=0;j<81;j++)
          	printf("%d",j1.board[j]);		
	   printf("\n");
        }
			
    }
}

int main(int argc, char* argv[])
{
  
  if (argv[1] != NULL)
  	numOfSolveThread = atoi(argv[1]);

  pthread_t ReaderThread;
  pthread_t SolveThread[numOfSolveThread];
  int64_t start,end;
  
  while(scanf("%s",fileName)!=EOF)
  {
	if(DEBUG_MODE)
  		printf("fileName: %s", fileName);
	
	if(pthread_create(&ReaderThread, NULL, ReaderFuction, NULL)!=0)
  	{
         	perror("pthread_create failed");
         	exit(1);
  	}
	pthread_join(ReaderThread, NULL); 

	start= now();
	
	for(int i=0;i<numOfSolveThread;i++)
  	{
    		if(pthread_create(&SolveThread[i], NULL, SolveFuction, NULL)!=0)
    		{
         		perror("pthread_create failed");
         		exit(1);
    		}
  	}
	
	for(int i=0;i<numOfSolveThread;i++)
      		pthread_join(SolveThread[i], NULL);  
	
        end = now();
  	double sec = (end-start)/1000000.0;
	if(DEBUG_MODE)
  		printf("%f sec %f ms each %d\n", sec, 1000*sec/total, total_solved);
	
	
	while(!result_queue.empty())
  	{
		job_t j1 = result_queue.top();
		result_queue.pop();
	        fprintf(stdout,"[%d] ",j1.No);
        	for(int j=0;j<N;j++)
            	fprintf(stdout,"%d",j1.board[j]);	
		fprintf(stdout,"\n");
	}
  
   }
   
  return 0;
}


