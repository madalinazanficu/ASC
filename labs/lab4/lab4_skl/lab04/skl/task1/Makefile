COMPILER=gcc
CFLAGS  = -std=c99 -g -Wall -O0
OPTIMIZE_FLAGS = -std=c99 -Wall -O3
LDLIBS  = -lm

%: %.c
	$(COMPILER) $(CFLAGS) $^ -o $@ $(LDLIBS)

optimize_%: %.c
	$(COMPILER) $(OPTIMIZE_FLAGS) $^ -o $* $(LDLIBS)

clean:
	rm -rf task1
