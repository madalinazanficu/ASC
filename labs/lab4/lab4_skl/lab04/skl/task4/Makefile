COMPILER=gcc
CFLAGS  = -std=c99 -g -Wall -O0
OPTIMIZE_FLAGS = -std=c99 -Wall -O3
LDLIBS  = -lm

%: %.c
	$(COMPILER) $(CFLAGS) $^ -o $@ $(LDLIBS)

optimize_%: %.c
	$(COMPILER) $(OPTIMIZE_FLAGS) $^ -o $* $(LDLIBS)

line_size.out : task4
	./line_size.sh > line_size.out

plot_line_size : line_size.out
	gnuplot -persist -e "set term svg; set output 'line_size.svg'; set xlabel 'Step (bytes)'; set ylabel 'Average time (sec/ops)'; plot 'line_size.out' using 1:4 title 'Cache line size'"

clean:
	rm -f line_size.out
	rm -f line_size.svg
	rm -rf task4
