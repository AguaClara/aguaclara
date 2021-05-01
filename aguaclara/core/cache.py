# The cache decorator does not support objects nested within datastructures or other objects. It is quite limited
# because the hash function is limited. This could be revisited and we could use a serialization library like Pickle
# if this proved to be an issue (which it most likely will when we get more complex classes)

import collections
import warnings

# The cache has key=(function name , parameter serialization) and value=
__ac_cache__ = {}


def ac_cache(method):
    def _cache(*args, **kw):
        global __cache__
        param_list = [args, kw]
        params_key = tuple([method.__name__, ac_hash(param_list)])
        try:
            value = __ac_cache__[params_key]
        except KeyError:
            value = method(*args, **kw)
            __ac_cache__[params_key] = value

        return value

    # Attempt to hash any object
    def ac_hash(hashable_object):
        if is_simple_hashable(hashable_object):
            a_hash = repr(hashable_object)
        elif isinstance(hashable_object, HashableObject):
            a_hash = hashable_object.ac_hash()
        elif isinstance(hashable_object, collections.Iterable):
            a_hash = ac_hash_iterable_into_tuple(hashable_object)
        else:
            a_hash = repr(hashable_object)
            warnings.warn("Using repr() to make a hash of {}. Please consider inheriting HashableObject class as repr "
                          "will not guarantee replicable hashing and can result in bad cache returns.".format(
                repr(hashable_object)), Warning, stacklevel=2)
        return a_hash

    def ac_hash_iterable_into_tuple(hashable_object_list):
        hash_tuple = ()
        for hashable_object in hashable_object_list:
            hash_tuple += (ac_hash(hashable_object),)
        return hash_tuple

    primitive = (int, str, bool, ...)
    def is_simple_hashable(thing):
        return type(thing) in primitive

    return _cache

class HashableObject:
    def ac_hash(self):
        return tuple(sorted(self.__dict__.items()))