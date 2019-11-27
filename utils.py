def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safe_cast_by_key(val, key, to_type, default=None):
    try:
        if key in val:
            return safe_cast(val[key], to_type, default)
        else:
            return default
    except TypeError:
        return default