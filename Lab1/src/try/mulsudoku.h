#ifndef MULSUDOKU_H
#define MULSUDOKU_H

const bool DEBUG_MODE = false;
enum { ROW=9, COL=9, N = 81, NEIGHBOR = 20 };
const int NUM = 9;

struct job_t
{
	int puzzleNo;	//题目在输入文件中的编号
	int board[81];  //题目
};
struct cmp
{
    bool operator() (job_t j1,job_t j2){
        return j1.puzzleNo > j2.puzzleNo;
    }
};
bool mulsolve_sudoku_dancing_links(int unused,job_t& job);
#endif
