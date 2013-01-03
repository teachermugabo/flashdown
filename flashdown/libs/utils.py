from django.shortcuts import _get_queryset

def get_and_delete(d, key, default):
    """
    Utility method to remove an entry for a dict and return it, returning the default value
    if d[key] doesn't exist or if it maps to None. Works similar to d.get(key, default) except that it
    removes the mapping as well. Used mainly to get and remove session data.
    """
    if key in d:
        result = d[key]
        del d[key]
        if result is not None:
            return result
        else:
            return default
    else:
        return default


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object, or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    qs = _get_queryset(klass) # makes get_object_or* more DRY
    try:
        return qs.get(*args, **kwargs)
    except qs.model.DoesNotExist:
        return None


