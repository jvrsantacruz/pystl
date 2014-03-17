# -*- coding: utf-8 -*-

from collections import Iterable

from nose.tools import assert_raises

from pystl import vector
from ._helpers import populated_raw_vector


class _TestConstructor(object):
    def test_it_should_create_an_empty_list(self):
        v = self.make_vector()

        assert list(v) == []

    def test_it_should_populate_vector_when_a_collection_is_given(self):
        l = range(1000)

        v = self.make_vector(l)

        assert list(v) == l

    def test_it_should_use_an_existing_vector_if_given(self):
        l = range(1000)
        v = self.make_vector()

        with populated_raw_vector(v, l) as cv:
            v = self.make_vector(ref=cv)

            assert list(v) == l


class _TestLen(object):
    def test_it_should_return_the_list_size(self):
        l = range(1000)

        v = self.make_vector(l)

        assert len(v) == len(l)

    def test_it_should_reflect_vector_growing(self):
        v = self.make_vector()

        assert len(v) == 0

        v.append(1)

        assert len(v) == 1

    def test_it_should_reflect_vector_shrinking(self):
        v = self.make_vector()

        v.append(1)
        assert len(v) == 1

        del v[0]
        assert len(v) == 0


class _TestGetItem(object):
    def test_it_should_return_the_nth_element(self):
        v = self.make_vector([1])

        assert v[0] == 1

    def test_it_should_count_from_back_with_negative_indexes(self):
        v = self.make_vector([1, 2])

        assert v[-1] == 2


class _TestGetItemSlice(object):
    def test_it_should_return_an_empty_list_when_slicing(self):
        v = self.make_vector()

        assert v[:] == []

    def test_it_should_return_the_whole_list_if_no_indexes_given(self):
        v = self.make_vector(range(10))

        assert v[:] == range(10)

    def test_it_should_return_the_list_from_the_start_if_no_start_is_given(self):
        v = self.make_vector(range(10))

        assert v[:5] == [0, 1, 2, 3, 4]

    def test_it_should_return_the_list_to_the_end_if_no_end_is_given(self):
        v = self.make_vector(range(10))

        assert v[5:] == [5, 6, 7, 8, 9]

    def test_it_should_return_a_list_from_start_to_end_when_slicing(self):
        v = self.make_vector(range(10))

        assert v[5:10] == [5, 6, 7, 8, 9]

    def test_negative_indexes_should_start_from_the_back(self):
        v = self.make_vector(range(10))

        assert v[-5: -1] == [5, 6, 7, 8]

    def test_it_should_use_step_to_select_the_numbers(self):
        v = self.make_vector(range(10))

        assert v[::2] == [0, 2, 4, 6, 8]

    def test_using_a_negative_step_should_return_reversed_list(self):
        v = self.make_vector(range(11))

        assert v[10:0:-1] == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    def test_using_bigger_indexes_does_not_explode(self):
        v = self.make_vector(range(11))

        assert v[0:5000:10] == [0, 10]


class _TestSetItem(object):
    def test_set_non_existing_position_should_raise_index_error(self):
        v = self.make_vector()

        with assert_raises(IndexError):
            assert v[0]

    def test_set_existing_position_should_change_its_value(self):
        v = self.make_vector(range(10))

        assert v[5] == 5
        v[5] = 500
        assert v[5] == 500


class _TestIter(object):
    def test_it_should_be_iterable(self):
        v = self.make_vector()

        assert isinstance(v, Iterable)

    def test_it_should_have_a_next_method(self):
        v = self.make_vector(range(10))

        iterable = v.__iter__()

        assert iterable.next() == 0

    def test_it_should_raise_stop_iteration_at_last_item(self):
        v = self.make_vector()

        iterable = v.__iter__()

        with assert_raises(StopIteration):
            iterable.next()

    def test_it_should_iterate_the_whole_object(self):
        v = self.make_vector(range(10))

        iterable = v.__iter__()

        assert list(iterable) == range(10)


class _TestDelItem(object):
    def test_it_should_raise_index_error_with_non_existing_index(self):
        v = self.make_vector()

        with assert_raises(IndexError):
            del v[0]

    def test_it_should_delete_element_on_index(self):
        v = self.make_vector(range(10))

        assert len(v) == 10
        assert 5 in v

        del v[5]

        assert len(v) == 9
        assert 5 not in v


class _TestDelSlice(object):
    def test_it_should_delete_no_elements_if_empty(self):
        v = self.make_vector()

        del v[:]

    def test_it_should_delete_all_elements_if_no_indexes_given(self):
        v = self.make_vector(range(10))

        assert len(v) == 10
        del v[:]
        assert len(v) == 0

    def test_it_should_delete_from_the_start_if_no_start_given(self):
        v = self.make_vector(range(5))

        assert list(v) == [0, 1, 2, 3, 4]
        del v[:3]
        assert list(v) == [3, 4]

    def test_it_should_delete_to_the_end_if_no_end_given(self):
        v = self.make_vector(range(5))

        assert list(v) == [0, 1, 2, 3, 4]
        del v[3:]
        assert list(v) == [0, 1, 2]

    def test_it_should_delete_using_negative_indexes(self):
        v = self.make_vector(range(5))

        assert list(v) == [0, 1, 2, 3, 4]
        del v[-5:3]
        assert list(v) == [3, 4]

    def test_it_should_delete_reverse_ranges(self):
        v = self.make_vector(range(5))

        assert list(v) == [0, 1, 2, 3, 4]
        del v[10:2]
        assert list(v) == [0, 1]


class _TestStr(object):
    def test_it_manages_empty_lists(self):
        v = self.make_vector()

        assert str(v) == "[]"

    def test_it_puts_all_the_numbers_in_the_string(self):
        v = self.make_vector(range(10))

        assert str(v) == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"


class _TestInsert(object):
    def test_it_should_insert_at_given_position(self):
        v = self.make_vector(range(5))

        assert v[3] == 3
        assert len(v) == 5

        v.insert(3, 10)

        assert v[3] == 10
        assert v[4] == 3
        assert len(v) == 6


class _TestAppend(object):
    def test_it_should_create_a_new_element_at_the_end(self):
        v = self.make_vector(range(5))

        assert v[-1] == 4
        assert len(v) == 5

        v.append(5)

        assert v[-1] == 5
        assert len(v) == 6


class _TestExtend(object):
    def test_it_should_append_multiple_elements_at_the_end(self):
        v = self.make_vector(range(5))

        assert v[-1] == 4
        assert len(v) == 5

        v.extend(i for i in range(5, 8))

        assert v[5:8] == [5, 6, 7]
        assert len(v) == 8


class _TestIndex(object):
    def test_it_should_return_the_position_of_a_value(self):
        v = self.make_vector(range(5))

        v[4] = 10
        assert v[4] == 10
        assert v.index(10) == 4


class _TestPop(object):
    def test_it_should_raise_index_error_if_empty(self):
        v = self.make_vector()

        with assert_raises(IndexError):
            v.pop()

    def test_it_should_remove_last_element(self):
        v = self.make_vector(range(5))

        assert v[-1] == 4
        assert len(v) == 5

        v.pop()

        assert v[-1] == 3
        assert len(v) == 4

    def test_it_should_return_last_element(self):
        v = self.make_vector(range(5))

        assert v.pop() == 4

    def test_it_should_remove_given_index(self):
        v = self.make_vector(range(5))

        assert v[3] == 3
        assert len(v) == 5

        assert v.pop(3) == 3

        assert v[3] == 4
        assert len(v) == 4

    def test_it_should_raise_index_error_with_bad_index(self):
        v = self.make_vector(range(5))

        with assert_raises(IndexError):
            v.pop(5)

    def test_it_should_remove_negative_indexes(self):
        v = self.make_vector(range(5))

        assert len(v) == 5
        assert v[-1] == 4

        assert v.pop(-1) == 4

        assert v[-1] == 3
        assert len(v) == 4


class _TestRemove(object):
    def test_it_should_raise_value_error_if_element_not_in_vector(self):
        v = self.make_vector(range(5))

        with assert_raises(ValueError):
            v.remove(5)

    def test_it_should_remove_value_from_vector(self):
        v = self.make_vector(range(5))

        assert len(v) == 5
        assert v[-1] == 4

        v.remove(4)

        assert v[-1] == 3
        assert len(v) == 4


class _TestCount(object):
    def test_it_should_return_0_if_element_not_present(self):
        v = self.make_vector(range(5))

        assert v.count(5) == 0

    def test_it_should_return_the_number_of_times_the_number_appears(self):
        v = self.make_vector([5] * 500)

        assert v.count(5) == 500


class _TestSort(object):
    def test_it_should_sort_the_vector_if_empty(self):
        v = self.make_vector()

        v.sort()

        assert list(v) == []

    def test_it_should_sort_the_vector_ascendent_in_place(self):
        v = self.make_vector([5, 4, 3, 2, 1, 0])

        v.sort()

        assert list(v) == [0, 1, 2, 3, 4, 5]


class _TestReverse(object):
    def test_it_should_reverse_the_vector_in_place(self):
        v = self.make_vector([0, 1, 2, 3, 4, 5])

        v.reverse()

        assert list(v) == [5, 4, 3, 2, 1, 0]


class _TestEqual(object):
    def test_it_should_return_equal_if_both_empty(self):
        v1, v2 = self.make_vector(), self.make_vector()

        assert v1 == v2

    def test_it_should_return_true_if_they_are_equal(self):
        v1, v2 = self.make_vector(range(10)), self.make_vector(range(10))

        assert v1 == v2

    def test_it_should_return_false_if_they_are_different(self):
        v1, v2 = self.make_vector([0]), self.make_vector([1])

        assert not (v1 == v2)

    def test_it_should_return_false_if_not_its_type(self):
        v = self.make_vector()

        assert not (v == [])


class _TestNotEqual(object):
    def test_it_should_return_false_if_both_empty(self):
        v1, v2 = self.make_vector(), self.make_vector()

        assert not (v1 != v2)

    def test_it_should_return_false_if_they_are_equal(self):
        v1, v2 = self.make_vector(range(10)), self.make_vector(range(10))

        assert not (v1 != v2)

    def test_it_should_return_true_if_they_are_different(self):
        v1, v2 = self.make_vector([0]), self.make_vector([1])

        assert v1 != v2

    def test_it_should_return_false_if_not_its_type(self):
        v = self.make_vector()

        assert not (v != [])


class _Tests(_TestConstructor, _TestLen, _TestGetItem, _TestGetItemSlice,
             _TestSetItem, _TestIter, _TestDelItem, _TestDelSlice, _TestStr,
             _TestInsert, _TestAppend, _TestExtend, _TestIndex, _TestPop,
             _TestRemove, _TestCount, _TestSort, _TestReverse, _TestEqual,
             _TestNotEqual):
    pass


class _TestInt(object):
    def make_vector(self, *args, **kwargs):
        return vector.VectorInt(*args, **kwargs)


class _TestLong(object):
    def make_vector(self, *args, **kwargs):
        return vector.VectorLong(*args, **kwargs)


class TestIntegerVector(_TestInt, _Tests):
    pass


class TestLongVector(_TestLong, _Tests):
    pass
