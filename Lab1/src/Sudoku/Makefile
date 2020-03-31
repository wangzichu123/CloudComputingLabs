CXXFLAGS+=-O2 -ggdb -DDEBUG
CXXFLAGS+=-Wall -Wextra

all: sudoku sudoku_solve

sudoku: main.cc neighbor.cc sudoku_basic.cc sudoku_min_arity.cc sudoku_min_arity_cache.cc sudoku_dancing_links.cc
	g++ -O2 -o $@ $^
	
sudoku_solve: main_multhr.cc  sudoku_dancing_links_multhr.cc
	g++ -O2 -pthread -o $@ $^
