#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#include "sudokumulthr.h"

// sudoku content
char (*sudoku_content)[N];
// sudoku result
int (*sudoku_result)[N];

int sudoku_Num = 0;
int current_job = 0;

typedef struct {
  	int thr_board[N];
}Threadboard;

pthread_mutex_t job_mutex = PTHREAD_MUTEX_INITIALIZER;

int64_t now ()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec * 1000000 + tv.tv_usec;
}

// Get board
void get_board(const char get[N],int *board) {
  	for (int i = 0;i < N;i++) {
    	board[i] = get[i] - '0';
    	assert(0 <= board[i] && board[i] <= NUM);
  	}
}

// Assign job
int assign() {
    pthread_mutex_lock(&job_mutex);
     // Finish
    if(current_job >= sudoku_Num)
    {
      pthread_mutex_unlock(&job_mutex);
      return -1;
    }
    int assigned_job = current_job++;
    pthread_mutex_unlock(&job_mutex);
    return assigned_job;
}

// Sudoku solve
void* solve(void *args) {
	Threadboard* para = (Threadboard*) args; 
	int assigned_job = 0;
	while(1) {
		assigned_job = assign();
		// Finish
		if(assigned_job == -1)
        	break;
  		get_board(sudoku_content[assigned_job],para->thr_board);
  		solve_sudoku_dancing_links(para->thr_board,0);
  		for (int i=0;i<N;i++) {
  			sudoku_result[assigned_job][i] = para->thr_board[i];
  		}
  	}
}

int main(int argc, char* argv[])
{
	int thread_Num=8;
    	char fileName[128];
	pthread_t thr[thread_Num];
	Threadboard par[thread_Num];
	while (scanf("%s",fileName)!=EOF) {
		int64_t start = now();
		// Initialize the number of sudoku
		sudoku_Num=0;
		current_job=0;
    		char puzzle[128];
		FILE *file_pointer = fopen(fileName,"r");
		// Record the number of sudoku
		while (fgets(puzzle,sizeof puzzle,file_pointer) != NULL) {
			sudoku_Num++;
		}
		// Initialize content and result
		sudoku_content = (char (*)[N]) malloc(sudoku_Num*N*sizeof(int));
		sudoku_result = (int (*)[N]) malloc(sudoku_Num*N*sizeof(int));
		// Reset the file pointer to the head, in order to read data
		rewind(file_pointer);
		int j=0;
		// Record the content of sudoku
		while (fgets(puzzle,sizeof puzzle,file_pointer) != NULL) {
			strcpy(sudoku_content[j],puzzle);
			j++;
		}
		fclose(file_pointer);
		for(int i=0;i<thread_Num;i++) {
			// Creat pthreads
    		if(pthread_create(&thr[i],NULL,solve,&par[i])!=0) {
      			perror("pthread_create failed");
      			exit(1);
    		}
  		}
  		// wait
		for(int i=0;i<thread_Num;i++)
    		pthread_join(thr[i], NULL);
 		// output 
		for(int i=0;i<sudoku_Num;i++) {
			for(int j=0;j<N;j++) {
				fprintf(stdout,"%d",sudoku_result[i][j]);
			}
  		fprintf(stdout,"\n");
		fflush(stdout);
		}
  		free(sudoku_content);
  		free(sudoku_result);
 		int64_t end = now();
 		double time = (end-start)/1000000.0;
  		fprintf(stderr," %f sec\n",time);
    }
  	return 0;
}


