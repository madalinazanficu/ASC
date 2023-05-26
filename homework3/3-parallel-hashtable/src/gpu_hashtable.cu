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
	glbGpuAllocator->_cudaMalloc((void **)&(this->buckets), size * sizeof(struct data));
	if (this->buckets == NULL) {
		printf("Could not allocate memory");
	}
}

/**
 * Function desctructor GpuHashTable
 */
GpuHashTable::~GpuHashTable() {
	glbGpuAllocator->_cudaFree(this->buckets);
}


/**
 * Function reshape
 * Performs resize of the hashtable based on load factor
 */
void GpuHashTable::reshape(int numBucketsReshape) {

	// Allocate new memory (GPU/VRAM) for more buckets
	struct data *new_buckets = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(new_buckets),
									numBucketsReshape * sizeof(struct data));
	
	// Save the reference of the old buckets
	struct data *old_buckets = this->buckets;

	// Get all the keys and values from the old buckets
	int *keys = getAllKeys(this->size);
	int *values = getBatch(keys, this->size);

	// Update the hashtable fields
	this->hmax = numBucketsReshape;
	this->buckets = new_buckets;
	this->size = 0;

	// Insert all the elements from the old buckets to the new one
	insertBatch(keys, values, this->size);

	// Free old buckets
	glbGpuAllocator->_cudaFree(old_buckets);

	return;
}


__global__ void kernel_insert(int *keys, int *value, int numKeys,
								struct data *buckets, int size, int hmax) {

	int index = blockIdx.x * blockDim.x + threadIdx.x;

	int key = keys[index];
	int val = value[index];
	int pos = hash_function_int(&key) % hmax;
	int curr_pos = 0, ref_pos = 0;
	bool stop = false;

	switch (buckets[pos].key) {
	
	// Case 1: Empty bucket => insert key:value
	case 0:
		buckets[pos].key = key;
		buckets[pos].value = val;
		break;

	// Collision
	default:

		// Case 2:  Key already exists => update value
		if (buckets[pos].key == key) {
			buckets[pos].value = val;
			break;
		}
		
		// Case 3: key already exists but in another bucket => update value
		ref_pos = pos;
		curr_pos = (pos + 1) % hmax;
		stop = false;
		while (curr_pos != ref_pos) {
			if (buckets[curr_pos].key == key) {
				buckets[curr_pos].value = val;
				stop = true;
				break;
			}
			curr_pos = (curr_pos + 1) % size;
		}
		if (stop == true) {
			break;
		}

		// Case 4: find the next available slot
		while (buckets[pos].key != 0) {
			pos = (pos + 1) % size;
		}
		buckets[pos].key = key;
		buckets[pos].value = val;
		break;
	}
}

/**
 * Function insertBatch
 * Inserts a batch of key:value, using GPU and wrapper allocators
 */
bool GpuHashTable::insertBatch(int *keys, int* values, int numKeys) {

	cout << "Inserting batch" << endl;

	int available_space = this->hmax - this->size;

	// In case of not enough space, resize the hashtable
	if (available_space <= numKeys) {
		int new_size = this->hmax + numKeys;
		this->reshape(new_size);
	}

	int blocks = numKeys / 256;
	int threads = 256;
	kernel_insert<<<blocks, threads>>>(keys, values, numKeys, this->buckets,
										this->size, this->hmax);

	this->size += numKeys;
	return true;
}

__global__ void kernel_get_batch(int *keys, int num, struct data *buckets,
										int size, int hmax, int *result_vec) {
    
	int index = blockIdx.x * blockDim.x + threadIdx.x;
	int key = keys[index];
	int pos = hash_function_int(&key) % hmax;
	int result = 0;

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
			break;
		}
		curr_pos = (curr_pos + 1) % size;
	}
	result_vec[index] = result;
		
	return;
}

/**
 * Function getBatch
 * Gets a batch of key:value, using GPU
 */
int* GpuHashTable::getBatch(int* keys, int numKeys) {

	cout << "Getting batch" << endl;

	int blocks = numKeys / 256;
	int threads = 256;

	// Allocate memory (GPU/VRAM) for result vector
	int *result_vec_gpu = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(result_vec_gpu), numKeys * sizeof(int));


	// Each CPU kernel will write the result in the result vector
	kernel_get_batch<<<blocks, threads>>>(keys, numKeys, this->buckets,
										this->size, this->hmax, result_vec_gpu);


	// The returned result vector will be copied from GPU memory to host memory
	int *result_vec_cpu = (int *)malloc(numKeys * sizeof(int));
	cudaMemcpy(result_vec_cpu, result_vec_gpu,
				numKeys * sizeof(int),cudaMemcpyDeviceToHost);
	
	// Free memory (GPU/VRAM) for result vector
	glbGpuAllocator->_cudaFree(result_vec_gpu);


	// Final result from RAM
	return result_vec_cpu;
}



__global__ void kernel_get_keys(int numKeys, struct data *buckets,
									int size, int hmax, int *result_vec) {
	
	int index = blockIdx.x * blockDim.x + threadIdx.x;
	int key = buckets[index].key;

	if (key != 0) {
		result_vec[index] = key;
	}
		
	return;
}

int* GpuHashTable::getAllKeys(int numKeys) {
	
	cout << "Getting all keys" << endl;

	int blocks = numKeys / 256;
	int threads = 256;

	// Allocate memory (GPU/VRAM) for result vector
	int *result_vec_gpu = NULL;
	glbGpuAllocator->_cudaMalloc((void **)&(result_vec_gpu), numKeys * sizeof(int));

	// Each CPU kernel will write the result in the result vector
	kernel_get_keys<<<blocks, threads>>>(numKeys, this->buckets,
										this->size, this->hmax, result_vec_gpu);

	int *result_vec_cpu = (int *)malloc(numKeys * sizeof(int));
	cudaMemcpy(result_vec_cpu, result_vec_gpu,
				numKeys * sizeof(int),cudaMemcpyDeviceToHost);

	// Free memory (GPU/VRAM) for result vector
	glbGpuAllocator->_cudaFree(result_vec_gpu);

	// Final result from RAM
	return result_vec_cpu;
}
