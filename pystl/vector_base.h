#ifndef __PY_VECTOR_BASE__
#define __PY_VECTOR_BASE__

#include <vector>
#include <algorithm>

using namespace std;


template <typename T>
static vector<T> * py_vector_new() {
	return new vector<T>;
}

template <typename T>
static void py_vector_delete(vector<T> * pvector) {
	delete pvector;
}

template <typename T>
static size_t py_vector_size(vector<T> * pvector){
	return pvector->size();
}

template <typename T>
static T py_vector_at(vector<T> * pvector, size_t index) {
	return pvector->at(index);
}

template <typename T>
static void py_vector_set(vector<T> * pvector, size_t index, T value) {
    pvector->at(index) = value;
}

template <typename T>
void py_vector_push_back(vector<T> * pvector, T number) {
	pvector->push_back(number);
}

template <typename T>
void py_vector_insert(vector<T> * pvector, size_t index, T value) {
	pvector->insert(pvector->begin() + index, value);
}

template <typename T>
void py_vector_erase(vector<T> * pvector, size_t index) {
	pvector->erase(pvector->begin() + index);
}

template <typename T>
void py_vector_erase(vector<T> * pvector, size_t begin, size_t end) {
	pvector->erase(pvector->begin() + begin, pvector->begin() + end);
}

template <typename T>
int py_vector_find(vector<T> * pvector, T value) {
    typename vector<T>::iterator it;

    it = find(pvector->begin(), pvector->end(), value);

    if( it == pvector->end() )
        return -1;
    else
        return it - pvector->begin();  // index
}

template <typename T>
T py_vector_pop_back(vector<T> * pvector) {
    T back = pvector->back();
    pvector->pop_back();
    return back;
}

template <typename T>
size_t py_vector_count(vector<T> * pvector, T value) {
    return count(pvector->begin(), pvector->end(), value);
}

template <typename T>
void py_vector_sort(vector<T> * pvector) {
    return stable_sort(pvector->begin(), pvector->end());
}

template <typename T>
void py_vector_reverse(vector<T> * pvector) {
    return reverse(pvector->begin(), pvector->end());
}

template <typename T>
int py_vector_equal(vector<T> * pvector, vector<T> * pother) {
    return *pvector == *pother;
}

#endif
