import importlib


def get_model(module_location):
    """
    Returns the instance of the given module location.
    """

    if not isinstance(module_location, (str, unicode)):
        raise ValueError("The value provided should either be a string or "\
                "unicode instance. The value '%s' provided was %s "\
                "rather." % (module_location, type(module_location)))

    try:
        name_split = module_location.split(".")
        class_name = name_split.pop(-1)

        if not len(name_split):
            raise ValueError("The value should provide the module location "\
                    "joined by '.' e.g. for model named 'test' in "
                    "/app/module.py, The value should be 'app.module.test'")

        module_location = ".".join(name_split)
        module = importlib.import_module(module_location)
        cls = getattr(module, class_name)

        return cls

    except AttributeError:
        pass
