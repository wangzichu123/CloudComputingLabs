CXXFLAGS+=-O2 -ggdb -DDEBUG
CXXFLAGS+=-Wall -Wextra

all: sudoku_solve

sudoku_solve: mulmain.c  mulsudoku_dancing_links.cc
	g++ -O2 -pthread -o $@ $^
clean:	
	-rm sudoku_slove
