#ifndef __PY_VECTOR_LONG__
#define __PY_VECTOR_LONG__

#include "vector_base.h"

extern "C" {

	vector<long> * py_vector_long_new() { 
		return py_vector_new<long>(); 
	}

	void py_vector_long_delete(vector<long> * pvector) {
		py_vector_delete(pvector);
	}

	size_t py_vector_long_size(vector<long> * pvector){
		return py_vector_size(pvector);
	}

	long py_vector_long_at(vector<long> * pvector, size_t index) {
		return py_vector_at(pvector, index);
	}

	void py_vector_long_set(vector<long> * pvector, size_t index, long value) {
		py_vector_set(pvector, index, value);
	}

	void py_vector_long_push_back(vector<long> * pvector, long value) {
		py_vector_push_back(pvector, value);
	}

	void py_vector_long_insert(vector<long> * pvector, size_t index, long value) {
		py_vector_insert(pvector, index, value);
	}

	void py_vector_long_erase(vector<long> * pvector, size_t index) {
		py_vector_erase(pvector, index);
	}

	void py_vector_long_erase_slice(vector<long> * pvector, size_t begin, size_t end) {
		py_vector_erase(pvector, begin, end);
	}

	int py_vector_long_find(vector<long> * pvector, long value) {
		return py_vector_find(pvector, value);
	}

	long py_vector_long_pop_back(vector<long> * pvector){
		return py_vector_pop_back(pvector);
	}

    size_t py_vector_long_count(vector<long> * pvector, long value) {
            return py_vector_count(pvector, value);
        }

    void py_vector_long_sort(vector<long> * pvector) {
            py_vector_sort(pvector);
        }

    void py_vector_long_reverse(vector<long> * pvector) {
            py_vector_reverse(pvector);
        }

    int py_vector_long_equal(vector<long> * pvector, vector<long> * pother) {
            return py_vector_equal(pvector, pother);
        }

}

#endif
