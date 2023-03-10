class ModuleProxyCache(dict):
    def __missing__(self, key):
        if "." not in key:
            return __import__(key)

        module_name, class_name = key.rsplit(".", 1)

        module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(module, class_name)

        self[key] = handler

        return handler

_cache = ModuleProxyCache()

def import_string(path):
    """
    Path must be module.path.ClassName
    """
    result = _cache[path]
    return result
