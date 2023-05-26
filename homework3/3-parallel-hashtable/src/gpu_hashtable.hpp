#ifndef _HASHCPU_
#define _HASHCPU_

/**
 * Class GpuHashTable to implement functions
 */
class GpuHashTable
{

	struct data *buckets;
	unsigned int size;			    // the current number of entries in hashtable
	unsigned int hmax;             // maximum entries in hashtable


	public:
		GpuHashTable(int size);
		void reshape(int sizeReshape);

		bool insertBatch(int *keys, int* values, int numKeys);
		int* getBatch(int* key, int numItems);
		int* getAllKeys(int* numKeys);

		~GpuHashTable();
};

struct data {
	unsigned int key;
	unsigned int value;
};

#endif
