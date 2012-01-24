# -*- coding: utf-8 -*-

class FormatRegistry(object):
    def __init__(self):
        self._loaded = False
        self.registry = {}
    
    def _load(self):
        if self._loaded:
            return
        import pkg_resources
        from notpil.incubator.formats import INCUBATOR_FORMATS
        self.registry.update({entry_point.name: entry_point.load() for entry_point in pkg_resources.iter_entry_points('notpil.formats')})
        self.registry.update(INCUBATOR_FORMATS)
        self._loaded = True
        
    def get_formats(self):
        self._load()
        return self.registry
    
    def get_format_objects(self):
        self._load()
        return self.registry.values()
    
    def get_format(self, format):
        self._load()
        return self.registry.get(format, None)

registry = FormatRegistry()
get_formats = registry.get_formats
get_format_objects = registry.get_format_objects
get_format = registry.get_format