all: gpu_hashtable

gpu_hashtable: src/*.cu
	nvcc -O2 -g -std=c++11 -I. -I./src *.cu ./src/*.cu -o gpu_hashtable

run:
	python bench.py

clean:
	rm -rf gpu_hashtable
	rm -rf slurm-*
