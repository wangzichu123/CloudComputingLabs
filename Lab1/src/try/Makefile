CXXFLAGS+=-O2 -ggdb -DDEBUG
CXXFLAGS+=-Wall -Wextra

all: sudoku_solve

sudoku_solve: main1.c  sudoku_dancing_links.cc
	g++ -O2 -pthread -o $@ $^
clean:	
	-rm sudoku_solve
