#ifndef __PY_VECTOR_INT__
#define __PY_VECTOR_INT__

#include "vector_base.h"

extern "C" {

	vector<int> * py_vector_int_new() { 
		return py_vector_new<int>(); 
	}

	void py_vector_int_delete(vector<int> * pvector) {
		py_vector_delete(pvector);
	}

	size_t py_vector_int_size(vector<int> * pvector){
		return py_vector_size(pvector);
	}

	int py_vector_int_at(vector<int> * pvector, size_t index) {
		return py_vector_at(pvector, index);
	}

	void py_vector_int_set(vector<int> * pvector, size_t index, int value) {
		py_vector_set(pvector, index, value);
	}

	void py_vector_int_push_back(vector<int> * pvector, int value) {
		py_vector_push_back(pvector, value);
	}

	void py_vector_int_insert(vector<int> * pvector, size_t index, int value) {
		py_vector_insert(pvector, index, value);
	}

	void py_vector_int_erase(vector<int> * pvector, size_t index) {
		py_vector_erase(pvector, index);
	}

	void py_vector_int_erase_slice(vector<int> * pvector, size_t begin, size_t end) {
		py_vector_erase(pvector, begin, end);
	}

	int py_vector_int_find(vector<int> * pvector, int value) {
		return py_vector_find(pvector, value);
	}

	int py_vector_int_pop_back(vector<int> * pvector){
		return py_vector_pop_back(pvector);
	}

    int py_vector_int_count(vector<int> * pvector, int value) {
            return py_vector_count(pvector, value);
        }

    void py_vector_int_sort(vector<int> * pvector) {
            py_vector_sort(pvector);
        }

    void py_vector_int_reverse(vector<int> * pvector) {
            py_vector_reverse(pvector);
        }

    int py_vector_int_equal(vector<int> * pvector, vector<int> * pother) {
            return py_vector_equal(pvector, pother);
        }

}

#endif
