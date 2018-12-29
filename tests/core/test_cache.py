from aguaclara.core.cache import ac_cache, HashableObject


class ComputedObject(HashableObject):
    def __init__(self):
        self.a = 2
        self.b = 3
        self.c = 4

    @property
    @ac_cache
    def product(self):
        increment_n_calls()
        return self.a * self.b * self.c

    @property
    @ac_cache
    def sum(self):
        increment_n_calls()
        return self.a + self.b + self.c

    @ac_cache
    def sum_with_arg(self, my_arg):
        increment_n_calls()
        return self.sum + my_arg

    @ac_cache
    def sum_with_kwarg(self, my_arg=10):
        increment_n_calls()
        return self.sum + my_arg


# Keep track of the total number of calls
side_effect_n_calls = 0


def increment_n_calls():
    global side_effect_n_calls
    side_effect_n_calls = side_effect_n_calls +1


def test_ac_cache():
    my_computed_object = ComputedObject()
    assert 24 == my_computed_object.product
    assert 1 == side_effect_n_calls
    assert 9 == my_computed_object.sum
    assert 2 == side_effect_n_calls
    assert 9 == my_computed_object.sum
    assert 2 == side_effect_n_calls
    my_computed_object.a=3
    assert 36 == my_computed_object.product
    assert 3 == side_effect_n_calls
    assert 10 == my_computed_object.sum
    assert 4 == side_effect_n_calls
    assert 15 == my_computed_object.sum_with_arg(5)
    assert 5 == side_effect_n_calls
    assert 20 == my_computed_object.sum_with_kwarg()
    assert 6 == side_effect_n_calls
    assert 20 == my_computed_object.sum_with_kwarg()
    assert 6 == side_effect_n_calls
    assert 25 == my_computed_object.sum_with_kwarg(my_arg=15)
    assert 7 == side_effect_n_calls
