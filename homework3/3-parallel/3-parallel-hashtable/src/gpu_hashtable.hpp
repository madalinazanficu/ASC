#ifndef _HASHCPU_
#define _HASHCPU_

/**
 * Class GpuHashTable to implement functions
 */

struct data {
	unsigned int key;
	unsigned int value;
};

class GpuHashTable
{
	struct data *buckets;
	unsigned int size;			    			// the current number of entries in hashtable
	unsigned int hmax;             				// maximum entries in hashtable
	const float max_threshold = 0.8f;  			// used to check if we need to resize
	const float regular_threshold = 0.6f;		// used to get a specific load factor for the hashtable

	public:
		GpuHashTable(int size);
		void reshape(int sizeReshape);

		bool insertBatch(int *keys, int* values, int numKeys);
		int* getBatch(int* key, int numItems);

		~GpuHashTable();
};

#endif
