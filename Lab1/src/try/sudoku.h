#ifndef MULSUDOKU_H
#define MULSUDOKU_H

const bool DEBUG_MODE = true;
enum { ROW=9, COL=9, N = 81, NEIGHBOR = 20 };
const int NUM = 9;

bool solve_sudoku_dancing_links(int unused,int *board);
#endif
