#include <iostream>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctime>
#include <sstream>
#include <string>
#include "test_map.hpp"
#include "gpu_hashtable.hpp"

using namespace std;

__host__ __device__ unsigned int hash_function_int(void *a)
{
	/*
	 * Credits: https://stackoverflow.com/a/12996028/7883884
	 * SD Laboratory
	 */
	unsigned int uint_a = *((unsigned int *)a);

	uint_a = ((uint_a >> 16u) ^ uint_a) * 0x45d9f3b;
	uint_a = ((uint_a >> 16u) ^ uint_a) * 0x45d9f3b;
	uint_a = (uint_a >> 16u) ^ uint_a;
	return uint_a;
}

/*
Allocate CUDA memory only through glbGpuAllocator
cudaMalloc -> glbGpuAllocator->_cudaMalloc
cudaMallocManaged -> glbGpuAllocator->_cudaMallocManaged
cudaFree -> glbGpuAllocator->_cudaFree
*/

/**
 * Function constructor GpuHashTable
 * Performs init
 * Example on using wrapper allocators _cudaMalloc and _cudaFree
 */
GpuHashTable::GpuHashTable(int size) {
	this->size = 0;
	this->hmax = size;
	this->buckets = NULL;

	// Allocate memory (GPU/VRAM) for buckets
	glbGpuAllocator->_cudaMalloc((void **)&(this->buckets),
									size * sizeof(struct data));
	if (this->buckets == NULL) {
		DIE(1, "Could not allocate memory");
	}
}

/**
 * Function desctructor GpuHashTable
 */
GpuHashTable::~GpuHashTable() {
	glbGpuAllocator->_cudaFree(this->buckets);
}



__global__ void kernel_resize(struct data *old_buckets, struct data *new_buckets,
								int size, int old_hmax, int new_hmax) {

	int index = blockIdx.x * blockDim.x + threadIdx.x;
	if (index >= old_hmax) {
		return;
	}

	int key = old_buckets[index].key;
	if (key == 0) {
		return;
	}

	int val = old_buckets[index].value;
	int pos = hash_function_int(&key) % new_hmax;

	int compare_and_swap = atomicCAS(&(new_buckets[pos].key), 0, key);

	// Case 0 : Empty bucket => insert key:value (atomic operation)
	if (compare_and_swap == 0) {
		new_buckets[pos].value = val;
	} else {
		// Case 1 : Collision => find the next empty bucket
		while (atomicCAS(&(new_buckets[pos].key), 0, key) != 0) {
			pos = (pos + 1) % new_hmax;
		}
		new_buckets[pos].value = val;
	}
}


/**
 * Function reshape
 * Performs resize of the hashtable based on load factor
 */
void GpuHashTable::reshape(int numBucketsReshape) {
	struct data *new_buckets = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(new_buckets),
									numBucketsReshape * sizeof(struct data));
	int new_hmax = numBucketsReshape;

	// Parallelize the copy of the old buckets to the new ones
	int blocks = this->hmax / 256;
	int threads = 256;
	if (this->hmax % 256 != 0) {
		blocks++;
	}
	kernel_resize<<<blocks, threads>>>(this->buckets, new_buckets,
									this->size, this->hmax, new_hmax);
	cudaDeviceSynchronize();

	// Update the fields of the hashtable
	struct data *old_buckets = this->buckets;
	this->buckets = new_buckets;
	this->hmax = new_hmax;

	glbGpuAllocator->_cudaFree(old_buckets);

	return;
}


__global__ void kernel_insert(int *keys, int *value, int numKeys,
								struct data *buckets, int size, int hmax) {

	int index = blockIdx.x * blockDim.x + threadIdx.x;
	if (index >= numKeys) {
		return;
	}

	// (key, value) -> data to be inserted
	int key = keys[index];
	int val = value[index];
	int pos = hash_function_int(&key) % hmax;
	int curr_pos = 0, ref_pos = 0;
	
	// Atomic operation to see if the bucket is empty
	int compare_and_swap = atomicCAS(&(buckets[pos].key), 0, key);

	// Case 0 : Empty bucket => insert key:value (atomic operation)
	// Case 1 : Key already exists => update value
	if (compare_and_swap == 0 || compare_and_swap == key) {
		//atomicExch(&buckets[pos].value, val);
		buckets[pos].value = val;
		return;

	}

	// Case2: Collision
	ref_pos = pos;
	curr_pos = (pos + 1) % hmax;
	while (curr_pos != ref_pos) {
		compare_and_swap = atomicCAS(&(buckets[curr_pos].key), 0, key);

		// Case 2.1: key already exists but in another bucket -> update value
		// Case 2.2: key doesn't exist -> old key is 0
		if (compare_and_swap == key || compare_and_swap == 0) {
			//atomicExch(&buckets[curr_pos].value, val);
			buckets[curr_pos].value = val;
			return;
		}
		curr_pos = (curr_pos + 1) % hmax;
	}
}

/**
 * Function insertBatch
 * Inserts a batch of key:value, using GPU and wrapper allocators
 */
bool GpuHashTable::insertBatch(int *keys, int* values, int numKeys) {
	int new_size = 0;

	// In case of not enough space, resize the hashtable
	float old_factor = (float)(this->size + numKeys) / (float)this->hmax;
	if (old_factor > this->max_threshold) {
		new_size = (this->size + numKeys) /this->regular_threshold;
		this->reshape(new_size);
	}

	// Allocate memory on GPU for keys and values
	int *d_keys = NULL;
	int *d_values = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(d_keys), numKeys * sizeof(int));
	cudaMemcpy(d_keys, keys, numKeys * sizeof(int), cudaMemcpyHostToDevice);

	glbGpuAllocator->_cudaMalloc((void **)&(d_values), numKeys * sizeof(int));
	cudaMemcpy(d_values, values, numKeys * sizeof(int), cudaMemcpyHostToDevice);


	// Insert the batch of keys and values
	int blocks = numKeys / 256;
	int threads = 256;
	if (numKeys % 256 != 0) {
		blocks++;
	}
	kernel_insert<<<blocks, threads>>>(d_keys, d_values, numKeys, this->buckets,
										this->size, this->hmax);
	cudaDeviceSynchronize();

	this->size += numKeys;

	// Free memory on GPU
	glbGpuAllocator->_cudaFree(d_keys);
	glbGpuAllocator->_cudaFree(d_values);

	return true;
}


__global__ void kernel_get_batch(int *keys, int num, struct data *buckets,
										int size, int hmax, int *result_vec) {
    
	int index = blockIdx.x * blockDim.x + threadIdx.x;
	if (index >= num) {
		return;
	}


	int key = keys[index];
	int pos = hash_function_int(&key) % hmax;
	int result = -1;

	if (buckets[pos].key == key) {
		result = buckets[pos].value;
		result_vec[index] = result;
		return;
	}

	int ref_pos = pos;
	int curr_pos = (pos + 1) % hmax;
	while (curr_pos != ref_pos) {
		if (buckets[curr_pos].key == key) {
			result = buckets[curr_pos].value;
			result_vec[index] = result;
			return;
		}
		// Can't find the key
		if (buckets[curr_pos].key == 0) {
			result_vec[index] = result;
			return;
		}
		curr_pos = (curr_pos + 1) % hmax;
	}
	result_vec[index] = result;
		
	return;
}


/**
 * Function getBatch
 * Gets a batch of key:value, using GPU
 */
int* GpuHashTable::getBatch(int* keys, int numKeys) {

	int blocks = numKeys / 256;
	int threads = 256;
	if (numKeys % 256 != 0) {
		blocks++;
	}

	// Allocate memory (GPU/VRAM) for result vector
	int *result_vec_gpu = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(result_vec_gpu), numKeys * sizeof(int));

	// Allocate memory (GPU/VRAM) for keys
	int *d_keys = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(d_keys), numKeys * sizeof(int));
	cudaMemcpy(d_keys, keys, numKeys * sizeof(int), cudaMemcpyHostToDevice);

	// Each CPU kernel will write the result in the result vector
	kernel_get_batch<<<blocks, threads>>>(d_keys, numKeys, this->buckets,
										this->size, this->hmax, result_vec_gpu);

	cudaDeviceSynchronize();

	// The returned result vector will be copied from GPU memory to host memory
	int *result_vec_cpu = (int *)malloc(numKeys * sizeof(int));
	cudaMemcpy(result_vec_cpu, result_vec_gpu,
				numKeys * sizeof(int),cudaMemcpyDeviceToHost);
	
	// Free memory (GPU/VRAM) for result vector
	glbGpuAllocator->_cudaFree(result_vec_gpu);
	glbGpuAllocator->_cudaFree(d_keys);

	// Final result from RAM
	return result_vec_cpu;
}