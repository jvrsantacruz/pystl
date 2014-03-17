# -*- coding: utf-8 -*-

from ._helpers import Spy, patch
from nose.tools import assert_raises

from pystl import Vector


def make_vector(*args, **kwargs):
    patch(
        Vector,
        vector_new=Spy(),
        vector_delete=Spy(),
        vector_size=Spy(),
        vector_at=Spy(),
        vector_set=Spy(),
        vector_push_back=Spy(),
        vector_insert=Spy(),
        vector_erase=Spy(),
        vector_erase_slice=Spy(),
        vector_find=Spy(),
        vector_pop_back=Spy(),
        vector_count=Spy(),
        vector_sort=Spy(),
        vector_reverse=Spy(),
        vector_equal=Spy()
    )

    v = Vector(*args, **kwargs)

    return v


class TestConstructor(object):
    def test_it_should_create_a_vector_if_no_ref_is_given(self):
        v = make_vector()

        assert v.vector_new.called

    def test_it_should_be_managed_if_no_ref_is_given(self):
        v = make_vector()

        assert v.managed is True

    def test_it_should_populate_vector_when_a_collection_is_given(self):
        v = make_vector([1, 2, 3])

        assert v.vector_push_back.number_of_calls == 3

    def test_it_should_not_be_managed_if_ref_is_given(self):
        v = make_vector(ref=1)

        assert v.managed is False

    def test_it_should_be_managed_if_ref_is_given_and_managed_overriden(self):
        v = make_vector(ref=1, managed=True)

        assert v.managed is True

    def test_it_should_not_create_new_vector_if_ref_is_given(self):
        v = make_vector(ref=1)

        assert v.vector_new.called is False

    def test_it_should_use_given_ref_as_vector(self):
        ref = 1

        v = make_vector(ref=ref)

        assert v.vector is ref


class TestDestructor(object):
    def test_it_should_delete_the_vector_if_managed(self):
        vector_delete = Spy()
        v = make_vector()
        patch(v, vector_delete=vector_delete)

        del v

        assert vector_delete.called

    def test_it_should_not_delete_the_vector_if_not_managed(self):
        vector_delete = Spy()
        v = make_vector(ref=1)
        patch(v, vector_delete=vector_delete)

        del v

        assert vector_delete.called is False


class TestLen(object):
    def test_it_should_call_vector_size_for_the_size(self):
        v = make_vector()
        v.vector_size.returns = 0

        len(v)

        assert v.vector_size.called

    def test_it_should_return_the_list_size(self):
        size = 5
        v = make_vector()
        v.vector_size.returns = size

        assert len(v) == size


class TestGetItem(object):
    def test_it_should_raise_index_error_if_vector_is_empty(self):
        v = make_vector()
        v.vector_size.returns = 0

        with assert_raises(IndexError):
            v[0]

    def test_it_should_raise_index_error_if_index_bigger_than_vector_size(self):
        v = make_vector()
        v.vector_size.returns = 0

        with assert_raises(IndexError):
            v[1]

    def test_it_should_return_the_nth_element(self):
        v = make_vector()
        v.vector_at.returns = 1
        v.vector_size.returns = 1

        assert v[0] == 1

    def test_it_should_return_the_nth_element_from_the_back_with_negative_numbers(self):
        v = make_vector()
        v.vector_at.returns = 0
        v.vector_size.returns = 1

        v[-1]

        assert v.vector_at.call_args[1] == 0

    def test_it_should_raise_index_error_if_neg_index_bigger_than_vector_size(self):
        v = make_vector()
        v.vector_at.returns = -1
        v.vector_size.returns = 2

        with assert_raises(IndexError):
            v[-3]


class TestGetSlice(object):
    def test_it_should_not_raise_index_error_if_vector_is_empty(self):
        v = make_vector()
        v.vector_size.returns = 0

        assert v[:] == []

    def test_it_should_use_0_for_start_if_not_given(self):
        size, index, value = 1, 0, 1
        v = make_vector()
        v.vector_size.returns = size
        v.vector_at.returns = value

        assert v[:size] == [value]
        assert v.vector_at.call_args == (None, index)

    def test_it_should_use_size_for_end_if_not_given(self):
        size, index, value = 1, 0, 1
        v = make_vector()
        v.vector_size.returns = size
        v.vector_at.returns = value

        assert v[0:] == [value]
        assert v.vector_at.call_args == (None, 0)

    def test_it_should_handle_begin_beign_bigger_than_end(self):
        v = make_vector()
        v.vector_size.returns = 10

        assert v[100:-100] == []

    def test_it_should_handle_negative_steps(self):
        size, value = 10, 1
        v = make_vector()
        v.vector_size.returns = size
        v.vector_at.returns = value

        print(v[100:-100:-1])

        assert v[100:-100:-1] == [1 for i in range(10)]


class TestSetItem(object):
    def test_it_should_raise_index_error_if_vector_is_empty(self):
        size, index, value = 0, 1, 5
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v[index] = value

    def test_it_should_raise_index_error_if_index_bigger_than_vector_size(self):
        size, index, value = 1, 1, 5
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v[index] = value

    def test_it_should_raise_index_error_if_neg_index_bigger_than_vector_size(self):
        size, index, value = 2, -3, 1
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v[index] = value

    def test_it_should_call_vector_set_when_setting_the_nth_element(self):
        vector, size, index, value = None, 2, 1, 2
        v = make_vector()
        v.vector_size.returns = size

        v[index] = value

        assert v.vector_set.call_args == (vector, index, value)

    def test_it_should_call_vector_set_when_setting_from_the_back(self):
        vector, size, index, true_index, value = None, 3, -1, 2, 100
        v = make_vector()
        v.vector_size.returns = size

        v[index] = value

        assert v.vector_set.call_args == (vector, true_index, value)


class TestInsert(object):
    def test_it_should_raise_index_error_if_vector_is_empty(self):
        size, index, value = 0, 1, 5
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v.insert(index, value)

    def test_it_should_raise_index_error_if_index_bigger_than_vector_size(self):
        size, index, value = 1, 1, 5
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v.insert(index, value)

    def test_it_should_raise_index_error_if_neg_index_bigger_than_vector_size(self):
        size, index, value = 2, -3, 1
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            v.insert(index, value)

    def test_it_should_call_vector_insert_when_inserting(self):
        vector, size, index, value = None, 2, 1, 5
        v = make_vector()
        v.vector_size.returns = size

        v.insert(index, value)

        assert v.vector_insert.call_args == (vector, index, value)


class TestAppend(object):
    def test_it_should_call_push_back_when_appending(self):
        vector, value = None, 1
        v = make_vector()

        v.append(value)

        assert v.vector_push_back.call_args == (vector, value)


class TestExtend(object):
    def test_it_should_call_append_for_every_element_when_extending(self):
        vector, values = None, [1, 2, 3]
        v = make_vector()
        v.append = Spy()

        v.extend(values)

        assert v.append.number_of_calls == len(values)


class TestIter(object):
    def test_it_should_return_an_iterable(self):
        vector, values = None, [1, 1, 1]
        v = make_vector()
        v.vector_at.returns = 1
        v.vector_size.returns = 3

        assert list(v) == values


class TestDelItem(object):
    def test_it_should_raise_index_error_if_vector_is_empty(self):
        size, index = 0, 1
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            del v[index]

    def test_it_should_raise_index_error_if_index_bigger_than_vector_size(self):
        size, index = 1, 1
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            del v[index]

    def test_it_should_raise_index_error_if_neg_index_bigger_than_vector_size(self):
        size, index = 2, -3
        v = make_vector()
        v.vector_size.returns = size

        with assert_raises(IndexError):
            del v[index]

    def test_it_should_call_vector_erase_when_deleting_an_element(self):
        vector, size, index = None, 1, 0
        v = make_vector()
        v.vector_size.returns = size

        del v[index]

        assert v.vector_erase.call_args == (vector, index)


class TestDelItemSlice(object):
    def test_it_should_not_raise_when_deleting_with_empty_vector(self):
        size = 0
        v = make_vector()
        v.vector_size.returns = size

        del v[5000:5000]

    def test_it_should_call_vector_erase_slice_when_deleting_slice(self):
        size = 1
        v = make_vector()
        v.vector_size.returns = size

        del v[-5000:5000]

        assert v.vector_erase_slice.call_args == (None, 0, size)

    def test_it_should_check_begin_boundaries(self):
        v = make_vector()
        v.vector_size.returns = 10

        del v[-2:5]  # erase [5, 8)

        print(v.vector_erase_slice.call_args)

        assert v.vector_erase_slice.call_args == (None, 5, 8)

    def test_it_should_check_end_boundaries(self):
        v = make_vector()
        v.vector_size.returns = 10

        del v[100:-100]  # erase [0, 9]

        print(v.vector_erase_slice.call_args)

        assert v.vector_erase_slice.call_args == (None, 0, 10)


class TestIndex(object):
    def test_it_should_raise_value_error_if_element_is_not_present(self):
        element = 0
        v = make_vector()
        v.vector_find.returns = -1

        with assert_raises(ValueError):
            v.index(element)

    def test_it_should_return_index_of_element(self):
        element = 0
        v = make_vector()
        v.vector_find.returns = 1

        assert v.index(element) == 1


class TestPop(object):
    def test_it_should_raise_index_error_when_pop_from_empty_vector(self):
        v = make_vector()
        v.vector_size.returns = 0

        with assert_raises(IndexError):
            v.pop()

    def test_it_should_return_last_element_when_pop(self):
        v = make_vector()
        v.vector_size.returns = 1
        v.vector_pop_back.returns = 0

        value = v.pop()

        assert value == 0

    def test_it_should_raise_index_error_when_pop_with_index_out_of_range(self):
        v = make_vector()
        v.vector_size.returns = 1

        with assert_raises(IndexError):
            v.pop(1)

    def test_it_should_raise_index_error_when_pop_with_negative_index_out_of_range(self):
        v = make_vector()
        v.vector_size.returns = 1

        with assert_raises(IndexError):
            v.pop(-2)

    def test_it_should_return_nth_element_when_pop_with_index(self):
        v = make_vector()
        v.vector_size.returns = 2
        v.vector_at.returns = 0

        value = v.pop(0)

        assert value == 0

    def test_it_should_remove_nth_element_when_pop_with_index(self):
        v = make_vector()
        v.vector_size.returns = 2

        v.pop(0)

        assert v.vector_erase.called


class TestRemove(object):
    def test_it_should_raise_value_error_if_element_is_not_found(self):
        v = make_vector()
        v.vector_size.returns = 0
        v.vector_find.returns = -1

        with assert_raises(ValueError):
            v.remove(0)

    def test_it_should_call_erase_with_found_element_index(self):
        vector, index, element, size = None, 1, 0, 2
        v = make_vector()
        v.vector_size.returns = size
        v.vector_find.returns = index

        v.remove(element)

        assert v.vector_erase.call_args == (vector, index)


class TestCount(object):
    def test_it_should_return_the_number_of_elements_with_a_value(self):
        v = make_vector()
        v.vector_count.returns = 5

        value = v.count(0)

        assert value == 5

    def test_it_should_call_vector_count_with_the_wanted_element(self):
        vector, value = None, 0
        v = make_vector()

        v.count(0)

        assert v.vector_count.call_args == (vector, value)


class TestSort(object):
    def test_it_should_call_py_vector_sort_when_sorting(self):
        v = make_vector()

        v.sort()

        assert v.vector_sort.call_args == (None,)


class TestReverse(object):
    def test_it_should_call_py_vector_reverse_when_reversing(self):
        v = make_vector()

        v.reverse()

        assert v.vector_reverse.call_args == (None,)


class TestEq(object):
    def test_it_should_call_py_vector_equal_when_comparing(self):
        v1, v2 = make_vector(), make_vector()

        v1 == v2

        assert v1.vector_equal.call_args == (v1.vector, v2.vector)
