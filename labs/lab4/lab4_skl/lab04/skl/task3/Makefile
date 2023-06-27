COMPILER=gcc
CFLAGS  = -std=c99 -g -Wall -O0
OPTIMIZE_FLAGS = -std=c99 -Wall -O3
LDLIBS  = -lm

%: %.c
	$(COMPILER) $(CFLAGS) $^ -o $@ $(LDLIBS)

optimize_%: %.c
	$(COMPILER) $(OPTIMIZE_FLAGS) $^ -o $* $(LDLIBS)

layer_cache_%: task3
	./$@.sh > $@.out

plot_layer_%:
	gnuplot -persist -e "set term svg; set output 'layer_cache_$*.svg'; set xlabel 'Size (bytes)'; set ylabel 'Performance (ops/sec)'; plot 'layer_cache_$*.out' using 1:4 title 'L$* cache size' with lines"

clean:
	rm -f task3
	rm -f layer_cache_1.out
	rm -f layer_cache_2.out
	rm -f layer_cache_1.svg
	rm -f layer_cache_2.svg
